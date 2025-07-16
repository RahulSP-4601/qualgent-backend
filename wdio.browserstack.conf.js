require('dotenv').config();

exports.config = {
  user: process.env.BROWSERSTACK_USERNAME,
  key: process.env.BROWSERSTACK_ACCESS_KEY,

  specs: ['./tests/onboarding.spec.js'],
  services: ['browserstack'],
  capabilities: [{
    'bstack:options': {
      os: 'Windows',
      osVersion: '11',
      browserName: 'Chrome',
      browserVersion: 'latest',
      projectName: 'QualGent',
      buildName: 'BrowserStack AppWright Demo',
      sessionName: 'Onboarding flow test',
    },
  }],
  framework: 'mocha',
  reporters: ['spec'],
};
