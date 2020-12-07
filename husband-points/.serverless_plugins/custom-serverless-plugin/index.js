'use strict';

class TriggerLambda {
  constructor(serverless, options) {
    this.serverless = serverless;
    this.options = options;
    this.provider = this.serverless.getProvider('aws');

    this.hooks = {
      'after:deploy:deploy': this.triggerSetFunction.bind(this),
      'after:deploy:finalize': this.triggerUploadFunction.bind(this),
    };
  }

  triggerUploadFunction() {
    this.options.function = 'upload';
    this.serverless.cli.log('Running the upload function');
    return this.serverless.pluginManager.spawn('invoke', this.options.function);
  };

  triggerSetFunction() {
    this.options.function = 'set';
    this.serverless.cli.log('Running the set function');
    return this.serverless.pluginManager.spawn('invoke', this.options.function);
  };

}

module.exports = TriggerLambda;
