<?php
// Runs the official H5P PHP core (h5p-php-library, the code Moodle embeds as h5plib_v128) against a
// .h5p produced by the harness, with a stub platform:
//   mode "admin"   : empty platform, uploader allowed to install libraries (Moodle manager)
//   mode "teacher" : platform already has the vendored libraries, uploader may not install (teacher)
// Then replays the display-time filter (H5PCore::filterParameters) and reports real alterations.
// Usage: php official_validator.php <file.h5p> <vendor/libraries> <h5p-php-library dir> <admin|teacher>
[$_, $file, $libsDir, $core, $mode] = $argv;
foreach (['h5p.classes.php', 'h5p-file-storage.interface.php', 'h5p-default-storage.class.php',
          'h5p-development.class.php', 'h5p-metadata.class.php'] as $f) {
  require_once "$core/$f";
}
$GLOBALS['libsDir'] = $libsDir;
$GLOBALS['canInstall'] = $mode === 'admin';
$GLOBALS['installedAll'] = $mode === 'teacher';

function stubLib($machine, $major, $minor) {
  $dir = "{$GLOBALS['libsDir']}/$machine-$major.$minor";
  if (!file_exists("$dir/library.json")) return NULL;
  $lib = json_decode(file_get_contents("$dir/library.json"), TRUE);
  $lib['libraryId'] = crc32("$machine $major.$minor");
  $lib['semantics'] = @file_get_contents("$dir/semantics.json") ?: NULL;
  return $lib;
}

$overrides = [
  't' => 'return strtr($message, $replacements);',
  'setErrorMessage' => '$this->messages[] = "ERREUR [$code] $message";',
  'setInfoMessage' => '$this->messages[] = "INFO $message";',
  'getPlatformInfo' => 'return ["name" => "stub", "version" => "1", "h5pVersion" => "1"];',
  'getUploadedH5pFolderPath' => 'return $GLOBALS["tmpDir"];',
  'getUploadedH5pPath' => 'return $GLOBALS["tmpPath"];',
  'getWhitelist' => 'return $isLibrary ? "$defaultContentWhitelist $defaultLibraryWhitelist" : $defaultContentWhitelist;',
  'mayUpdateLibraries' => 'return $GLOBALS["canInstall"];',
  'getLibraryId' => 'return ($GLOBALS["installedAll"] && stubLib($machineName, $majorVersion, $minorVersion)) ? 1 : FALSE;',
  'loadLibrary' => 'return stubLib($machineName, $majorVersion, $minorVersion);',
  'loadLibrarySemantics' => '$l = stubLib($machineName, $majorVersion, $minorVersion); return $l ? $l["semantics"] : NULL;',
  'getOption' => 'return $default;',
  'loadAddons' => 'return [];',
  'libraryHasUpgrade' => 'return FALSE;',
  'hasPermission' => 'return TRUE;',
];
$ref = new ReflectionClass('H5PFrameworkInterface');
$code = "class StubFramework implements H5PFrameworkInterface {\n  public \$messages = [];\n";
foreach ($ref->getMethods() as $m) {
  $params = [];
  foreach ($m->getParameters() as $p) {
    $s = ($p->isPassedByReference() ? '&' : '') . '$' . $p->getName();
    if ($p->isOptional()) {
      $s .= ' = ' . var_export($p->isDefaultValueAvailable() ? $p->getDefaultValue() : NULL, TRUE);
    }
    $params[] = $s;
  }
  $body = $overrides[$m->getName()] ?? 'return NULL;';
  $code .= "  public function {$m->getName()}(" . implode(', ', $params) . ") { $body }\n";
}
eval($code . "}\n");

$work = sys_get_temp_dir() . '/h5pval-' . getmypid() . '-' . mt_rand();
@mkdir($work);
$GLOBALS['tmpPath'] = "$work/upload.h5p";
$GLOBALS['tmpDir'] = "$work/extract";
copy($file, $GLOBALS['tmpPath']);

$fw = new StubFramework();
$h5pC = new H5PCore($fw, "$work/storage", '/', 'fr', FALSE);
$validator = new H5PValidator($fw, $h5pC);
$ok = $validator->isValidPackage(FALSE, FALSE);
$result = ['valid' => (bool) $ok, 'messages' => array_values(array_unique($fw->messages)), 'altered' => []];

if ($ok) {
  $zip = new ZipArchive(); $zip->open($file);
  $h5p = json_decode($zip->getFromName('h5p.json'), TRUE);
  $raw = $zip->getFromName('content/content.json');
  foreach ($h5p['preloadedDependencies'] as $d) {
    if ($d['machineName'] === $h5p['mainLibrary']) $main = $d;
  }
  $content = ['library' => ['name' => $main['machineName'], 'machineName' => $main['machineName'],
              'majorVersion' => $main['majorVersion'], 'minorVersion' => $main['minorVersion']],
              'params' => $raw, 'id' => NULL, 'slug' => 'x', 'title' => $h5p['title'], 'filtered' => '',
              'embedType' => 'iframe'];
  $GLOBALS['installedAll'] = TRUE;  // display happens on a platform that has the libraries
  $fw->messages = [];
  $filtered = $h5pC->filterParameters($content);
  $a = json_decode($raw, TRUE); $b = json_decode($filtered, TRUE);
  $norm = function ($v) { return is_string($v) ? html_entity_decode($v, ENT_QUOTES | ENT_HTML5, 'UTF-8') : $v; };
  $diff = [];
  $cmp = function ($x, $y, $path) use (&$cmp, &$diff, $norm) {
    if (is_array($x) && is_array($y)) {
      foreach (array_unique(array_merge(array_keys($x), array_keys($y))) as $k) {
        if (!array_key_exists($k, $y)) $diff[] = "$path.$k supprimé";
        elseif (!array_key_exists($k, $x)) $diff[] = "$path.$k ajouté";
        else $cmp($x[$k], $y[$k], "$path.$k");
      }
    } elseif ($norm($x) !== $norm($y) && !(is_numeric($x) && is_numeric($y) && $x == $y)) {
      $diff[] = "$path modifié: " . mb_substr(json_encode($x, JSON_UNESCAPED_UNICODE), 0, 120) . ' -> '
        . mb_substr(json_encode($y, JSON_UNESCAPED_UNICODE), 0, 120);
    }
  };
  $cmp($a, $b, 'content');
  $result['altered'] = $diff;
  $result['filterMessages'] = array_values(array_unique($fw->messages));
}
echo json_encode($result, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT), "\n";
exec('rm -rf ' . escapeshellarg($work));
