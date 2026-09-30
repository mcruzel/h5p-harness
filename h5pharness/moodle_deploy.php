<?php
// Dépôt d'un paquet .h5p dans un cours d'un Moodle installé sur la même machine (lancé par h5pharness/moodle.py).
//
//   php moodle_deploy.php <moodle_dir> <request.json>
//
// request.json: {"h5p": chemin du paquet, "filename": nom du fichier dans Moodle, "name": titre de l'activité,
//   "course": id ou nom abrégé, "section": n°, "as": "activity"|"page"|"bank", "page": cmid ou nom d'une page
//   existante (facultatif), "bank": true pour ranger aussi le contenu dans la banque de contenus du cours et y lier
//   l'activité ou la page, "key": identifiant stable de la source, "visible": true|false,
//   "user": nom d'utilisateur (facultatif), "owner": enseignant à qui attribuer le contenu de banque (facultatif)}
// Réponse (stdout, une ligne JSON) : {"ok": true, "action": "created"|"updated", "cmid": …, "url": …,
//   "bank": {"id", "action", "url"} | null, "linked": bool, "warnings": […]} ou {"ok": false, "error": "…"}.
//
// Le paquet est déposé au nom d'un administrateur (par défaut) : seul le propriétaire du fichier décide si Moodle peut
// installer les bibliothèques H5P qu'il contient (capacité moodle/h5p:updatelibraries).

define('CLI_SCRIPT', true);

/**
 * Create or replace the course content bank item of this source (found again by its stable file name).
 *
 * @return array [\core_contentbank\content, 'created'|'updated']
 */
function h5pharness_bank(context $coursecontext, string $filename, string $name, string $path, stdClass $user): array {
    global $DB;
    $fs = get_file_storage();
    $cb = new \core_contentbank\contentbank();
    $itemid = $DB->get_field_sql("SELECT itemid FROM {files} WHERE contextid = ? AND component = 'contentbank'
                                     AND filearea = 'public' AND filename = ?", [$coursecontext->id, $filename],
                                  IGNORE_MULTIPLE);
    $draft = $fs->create_file_from_pathname(['contextid' => context_user::instance($user->id)->id, 'component' => 'user',
        'filearea' => 'draft', 'itemid' => file_get_unused_draft_itemid(), 'filepath' => '/', 'filename' => $filename,
        'userid' => $user->id], $path);
    if ($itemid && ($content = $cb->get_content_from_id((int) $itemid))) {
        $content->get_content_type_instance()->replace_content($draft, $content);
        $action = 'updated';
    } else {
        $content = $cb->create_content_from_file($coursecontext, $user->id, $draft);
        $action = 'created';
    }
    $content->set_name($name);
    $draft->delete();
    return [$content, $action];
}

function h5pharness_out(array $data, int $code = 0): void {
    fwrite(STDOUT, json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n");
    exit($code);
}

if ($argc < 3) {
    h5pharness_out(['ok' => false, 'error' => 'usage: php moodle_deploy.php <moodle_dir> <request.json>'], 1);
}
[$moodledir, $requestfile] = [$argv[1], $argv[2]];
if (!is_readable($moodledir . '/config.php')) {
    h5pharness_out(['ok' => false, 'error' => "config.php introuvable dans $moodledir"], 1);
}
$req = json_decode((string) file_get_contents($requestfile), true);
if (!is_array($req) || empty($req['h5p']) || !is_readable($req['h5p'])) {
    h5pharness_out(['ok' => false, 'error' => 'requête invalide ou paquet illisible'], 1);
}

require($moodledir . '/config.php');
require_once($CFG->dirroot . '/course/lib.php');
require_once($CFG->dirroot . '/course/modlib.php');
require_once($CFG->libdir . '/filelib.php');
require_once($CFG->libdir . '/resourcelib.php');

try {
    global $DB, $USER;
    $warnings = [];

    // Acting user: an administrator unless told otherwise.
    if (!empty($req['user'])) {
        $user = $DB->get_record('user', ['username' => $req['user'], 'deleted' => 0], '*', IGNORE_MISSING);
        if (!$user) {
            throw new moodle_exception('generalexceptionmessage', 'error', '', "utilisateur « {$req['user']} » inconnu");
        }
    } else {
        $user = get_admin();
    }
    \core\session\manager::set_user($user);

    // Course: id or short name.
    $ref = (string) ($req['course'] ?? '');
    $course = ctype_digit($ref) ? $DB->get_record('course', ['id' => (int) $ref])
        : $DB->get_record('course', ['shortname' => $ref]);
    if (!$course || $course->id == SITEID) {
        throw new moodle_exception('generalexceptionmessage', 'error', '', "cours « $ref » introuvable (id ou nom abrégé)");
    }
    $coursecontext = context_course::instance($course->id);
    if (!has_capability('moodle/course:manageactivities', $coursecontext)) {
        throw new moodle_exception('generalexceptionmessage', 'error', '', "{$user->username} n'a pas le droit d'ajouter "
            . "des activités dans ce cours (moodle/course:manageactivities) : utiliser un compte enseignant ou administrateur");
    }
    if (!has_capability('moodle/h5p:updatelibraries', \context_system::instance())) {
        $warnings[] = "{$user->username} ne peut pas installer de bibliothèques H5P : le contenu ne s'affichera que si "
            . "le site possède déjà les mêmes versions";
    }

    $fs = get_file_storage();
    $as = in_array($req['as'] ?? '', ['page', 'bank'], true) ? $req['as'] : 'activity';
    $bank = $as === 'bank' || !empty($req['bank']);
    $modname = $as === 'page' ? 'page' : 'h5pactivity';
    if ($as !== 'bank' && !$DB->get_field('modules', 'visible', ['name' => $modname])) {
        throw new moodle_exception('generalexceptionmessage', 'error', '', "le module $modname est désactivé sur ce site");
    }
    if ($as === 'page' && !array_key_exists('displayh5p', filter_get_globally_enabled())) {
        $warnings[] = "le filtre « Afficher H5P » est désactivé : la page montrera un lien au lieu de l'activité";
    }
    $filename = clean_param((string) ($req['filename'] ?? 'activite.h5p'), PARAM_FILE);
    $name = shorten_text(trim((string) ($req['name'] ?? 'Activité H5P')), 255);
    $key = (string) ($req['key'] ?? $filename);
    $idnumber = ($as === 'page' ? 'h5p-page:' : 'h5p:') . (core_text::strlen($key) > 90 ? sha1($key) : $key);
    $section = (int) ($req['section'] ?? 0);
    $visible = !isset($req['visible']) || $req['visible'] ? 1 : 0;
    $placeholder = '<div class="h5p-placeholder" contenteditable="false">@@PLUGINFILE@@/' . rawurlencode($filename)
        . '</div>';
    $filerecord = function (int $contextid, string $component, string $filearea) use ($filename, $user): array {
        return ['contextid' => $contextid, 'component' => $component, 'filearea' => $filearea, 'itemid' => 0,
            'filepath' => '/', 'filename' => $filename, 'userid' => $user->id];
    };

    // Content bank: the item is created or replaced first; activities and pages then point to it (an alias, as when a
    // teacher picks it in the file picker with « Lier au fichier »), so there is a single copy to update.
    $bankinfo = null;
    $repoid = null;
    $bankfile = null;
    if ($bank) {
        if (!has_capability('moodle/contentbank:upload', $coursecontext)) {
            throw new moodle_exception('generalexceptionmessage', 'error', '', "{$user->username} ne peut pas déposer "
                . "dans la banque de contenus de ce cours (moodle/contentbank:upload)");
        }
        [$content, $bankaction] = h5pharness_bank($coursecontext, $filename, $name, $req['h5p'], $user);
        if (!empty($req['owner'])) {
            // In the bank a teacher may only edit its own contents (manageowncontent); the file itself stays owned by the
            // depositing account, which is what lets Moodle install the libraries it contains.
            $ownerid = $DB->get_field('user', 'id', ['username' => $req['owner'], 'deleted' => 0]);
            if (!$ownerid) {
                throw new moodle_exception('generalexceptionmessage', 'error', '', "propriétaire « {$req['owner']} » inconnu");
            }
            $DB->set_field('contentbank_content', 'usercreated', $ownerid, ['id' => $content->get_id()]);
        }
        $bankfile = $content->get_file();
        $bankinfo = ['id' => (int) $content->get_id(), 'action' => $bankaction,
            'url' => (new moodle_url('/contentbank/view.php', ['id' => $content->get_id()]))->out(false)];
        $repoid = $DB->get_field_sql("SELECT ri.id FROM {repository_instances} ri
                                        JOIN {repository} r ON r.id = ri.typeid
                                       WHERE r.type = 'contentbank' AND r.visible = 1", [], IGNORE_MULTIPLE);
        if (!$repoid && $as !== 'bank') {
            $warnings[] = "le dépôt « Banque de contenus » est désactivé sur ce site : l'activité reçoit une copie du "
                . "contenu au lieu d'un lien";
        }
    }
    if ($as === 'bank') {
        h5pharness_out(['ok' => true, 'action' => $bankinfo['action'], 'as' => 'bank', 'cmid' => null,
            'course' => (int) $course->id, 'url' => $bankinfo['url'], 'bank' => $bankinfo, 'linked' => false,
            'warnings' => $warnings]);
    }
    // The file of the activity/page: an alias of the content bank file, or the package itself.
    $putfile = function (array $record) use ($fs, $req, $repoid, $bankfile) {
        if ($repoid && $bankfile) {
            $reference = file_storage::pack_reference(['contextid' => $bankfile->get_contextid(),
                'component' => 'contentbank', 'filearea' => 'public', 'itemid' => $bankfile->get_itemid(),
                'filepath' => $bankfile->get_filepath(), 'filename' => $bankfile->get_filename()]);
            return $fs->create_file_from_reference($record, $repoid, $reference);
        }
        return $fs->create_file_from_pathname($record, $req['h5p']);
    };

    // Target module: an existing page named by the agent, or the module this source created before (idnumber).
    $cm = null;
    if ($as === 'page' && !empty($req['page'])) {
        $pageref = (string) $req['page'];
        foreach (get_fast_modinfo($course)->get_instances_of('page') as $candidate) {
            if ((ctype_digit($pageref) && $candidate->id == (int) $pageref) || $candidate->name === $pageref) {
                $cm = $candidate;
                break;
            }
        }
        if (!$cm) {
            $names = array_map(fn($c) => "« {$c->name} » (id {$c->id})",
                array_values(get_fast_modinfo($course)->get_instances_of('page')));
            throw new moodle_exception('generalexceptionmessage', 'error', '', "page « $pageref » introuvable dans le cours"
                . ($names ? ' ; pages : ' . implode(', ', $names) : ' (aucune page)'));
        }
    } else {
        $existing = $DB->get_record_sql(
            "SELECT cm.id FROM {course_modules} cm JOIN {modules} m ON m.id = cm.module
              WHERE cm.course = ? AND cm.idnumber = ? AND m.name = ? AND cm.deletioninprogress = 0",
            [$course->id, $idnumber, $modname], IGNORE_MULTIPLE);
        if ($existing) {
            $cm = get_fast_modinfo($course)->get_cm($existing->id);
        }
    }

    if ($cm) {
        // Update in place: same module, new package (Moodle redeploys it when its content changes).
        $context = context_module::instance($cm->id);
        if ($as === 'activity') {
            $fs->delete_area_files($context->id, 'mod_h5pactivity', 'package');
            $putfile($filerecord($context->id, 'mod_h5pactivity', 'package'));
            $DB->update_record('h5pactivity', (object) ['id' => $cm->instance, 'name' => $name, 'timemodified' => time()]);
        } else {
            $page = $DB->get_record('page', ['id' => $cm->instance], '*', MUST_EXIST);
            if ($old = $fs->get_file($context->id, 'mod_page', 'content', 0, '/', $filename)) {
                $old->delete();
            }
            $putfile($filerecord($context->id, 'mod_page', 'content'));
            $content = $page->content;
            if (strpos($content, '@@PLUGINFILE@@/' . rawurlencode($filename)) === false) {
                $content .= "\n" . $placeholder;   // added to a page written by someone else: keep what is there
            }
            $update = ['id' => $page->id, 'content' => $content, 'revision' => $page->revision + 1,
                'timemodified' => time()];
            if (empty($req['page'])) {
                $update['name'] = $name;
            }
            $DB->update_record('page', (object) $update);
        }
        rebuild_course_cache($course->id, true);
        $action = 'updated';
        $cmid = $cm->id;
    } else {
        course_create_sections_if_missing($course, $section);
        $mi = (object) [
            'modulename' => $modname, 'course' => $course->id, 'section' => $section, 'visible' => $visible,
            'name' => $name, 'cmidnumber' => $idnumber,
            'introeditor' => ['text' => '', 'format' => FORMAT_HTML, 'itemid' => 0],
        ];
        if ($as === 'activity') {
            $draftid = file_get_unused_draft_itemid();
            $putfile(['contextid' => context_user::instance($user->id)->id, 'component' => 'user',
                'filearea' => 'draft', 'itemid' => $draftid, 'filepath' => '/', 'filename' => $filename,
                'userid' => $user->id]);
            $config = get_config('h5pactivity');
            $core = (new \core_h5p\factory())->get_core();
            $mi->packagefile = $draftid;
            $mi->enabletracking = 1;
            $mi->grademethod = $config->grademethod ?? 1;
            $mi->reviewmode = $config->reviewmode ?? 1;
            $mi->grade = $CFG->gradepointdefault ?? 100;
            $mi->displayoptions = \core_h5p\helper::get_display_options($core,
                \core_h5p\helper::decode_display_options($core));
        } else {
            $mi->content = $placeholder;
            $mi->contentformat = FORMAT_HTML;
            $mi->display = RESOURCELIB_DISPLAY_OPEN;
            $mi->printintro = 0;
            $mi->printlastmodified = 0;
            $mi->revision = 1;
        }
        $info = create_module($mi);
        $cmid = $info->coursemodule;
        if ($as === 'page') {
            $context = context_module::instance($cmid);
            $putfile($filerecord($context->id, 'mod_page', 'content'));
        }
        $action = 'created';
    }
    $url = (new moodle_url('/mod/' . $modname . '/view.php', ['id' => $cmid]))->out(false);
    h5pharness_out(['ok' => true, 'action' => $action, 'as' => $as, 'cmid' => (int) $cmid, 'course' => (int) $course->id,
        'url' => $url, 'bank' => $bankinfo, 'linked' => (bool) ($repoid && $bankfile), 'warnings' => $warnings]);
} catch (Throwable $e) {
    $msg = $e instanceof moodle_exception && !empty($e->a) && is_string($e->a) ? $e->a : $e->getMessage();
    h5pharness_out(['ok' => false, 'error' => $msg], 1);
}
