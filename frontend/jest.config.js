const lodash = require('lodash')

const config = {
  verbose: true,
  preset: '@vue/cli-plugin-unit-jest',
  globals: {
    '_': lodash
  }
};

module.exports = config;
