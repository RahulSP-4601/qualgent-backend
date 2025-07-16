require('dotenv').config();

exports.config = {
  user: process.env.BROWSERSTACK_USERNAME,
  key: process.env.BROWSERSTACK_ACCESS_KEY,

  specs: ['./tests/onboarding.spec.js'],
  services: ['browserstack'],
  capabilities: [{
    'bstack:options': {
      deviceName: 'iPhone 14',
      osVersion: '16',
      realMobile: true,
      projectName: 'QualGent',
      buildName: 'BrowserStack iOS Demo',
      sessionName: 'iOS onboarding test'
    },
    browserName: 'Safari'
  }],
  framework: 'mocha',
  reporters: ['spec'],
};
