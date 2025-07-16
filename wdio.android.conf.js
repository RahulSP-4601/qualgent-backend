require('dotenv').config();

exports.config = {
  user: process.env.BROWSERSTACK_USERNAME,
  key: process.env.BROWSERSTACK_ACCESS_KEY,

  specs: ['./tests/onboarding.spec.js'],
  services: ['browserstack'],
  capabilities: [{
    'bstack:options': {
      deviceName: 'Samsung Galaxy S23',
      osVersion: '13.0',
      realMobile: true,
      projectName: 'QualGent',
      buildName: 'BrowserStack Android Demo',
      sessionName: 'Android onboarding test'
    },
    browserName: 'Chrome'
  }],
  framework: 'mocha',
  reporters: ['spec'],
};
