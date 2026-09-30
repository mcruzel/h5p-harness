var H5PUpgrades = H5PUpgrades || {};

/**
 * Upgrades for the Game Map content type.
 */
H5PUpgrades['H5P.Tabs'] = (() => {
  return {
    1: {
      /**
       * @param {object} parameters Content parameters.
       * @param {function} finished Callback when finished.
       * @param {object} extras Extra parameters such as metadata, etc.
       */
      3: (parameters, finished, extras) => {
        if (parameters?.behaviour?.colorBase) {
          delete parameters.behaviour.colorBase;
        }

        if (parameters?.behaviour?.colorBackground) {
          delete parameters.behaviour.colorBackground;
        }

        finished(null, parameters, extras);
      },
    },
  };
})();
