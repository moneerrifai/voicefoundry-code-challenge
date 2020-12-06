'use strict';

class TriggerLambda {
  constructor(serverless, options) {
    this.serverless = serverless;
    this.options = options;
    this.provider = this.serverless.getProvider('aws');


    // probably don't need this because it won't be actually used as a command
    this.commands = {
      triggerAfterDeploy: {
        usage: 'Triggers the upload Lambda function',
        lifecycleEvents: ['trigger'],
      },
    };

    // hooks section: the key is where I hook into here. My options are:
    // triggerAfterDeploy:trigger this is referencing the plugin itself
    // or some built-in hook. i am choosing after:deploy:finalize which is what the s3 also chooses
    // you can also do after:deploy:deploy
    
    this.hooks = {
      'after:deploy:deploy': this.triggerSetFunction.bind(this),
      'after:deploy:finalize': this.triggerUploadFunction.bind(this),
      // 'triggerAfterDeploy:trigger': this.triggerUploadFunction.bind(this),
      // 'after:deploy:finalize': this.triggerUploadFunction.bind(this),
    };
  }
//'after:deploy:finalize': this.triggerUploadFunction.bind(this),
  // might have to use this hook instead; after:aws:deploy:finalize:cleanup

  // the function itself - my options are:

  // something like this: 

  // function triggerUploadFunction (serverless) {
  //   let myfunction = serverless.service.function
  //   execute the lambda somehow in here
  // }

  // or

  // define a function where you call pluginManager and spawn ('invoke')


  triggerUploadFunction() {
    this.options.function = 'upload';
    this.serverless.cli.log('Running the upload function');
    return this.serverless.pluginManager.spawn('invoke', this.options.function).then(this.serverless.cli.log('Upload data to data S3 bucket complete'));
  };

  triggerSetFunction() {
    this.options.function = 'set';
    this.serverless.cli.log('Running the set function');
    return this.serverless.pluginManager.spawn('invoke', this.options.function).then(this.serverless.cli.log('Upload HTML file to website S3 bucket complete'));
  };

  // this should work
  // async triggerUploadFunction(serverless) {
  //   const prams = {};
  //   this.provider.request('Lambda', 'invoke', params);
  // }

  // this.provider.request('Lambda', 'invoke', params);
  // public async runMigration(): Promise<void> {
  //   const lambdaName = get(this.serverless.service, 'functions.migrator.name', '')
  //   const lambdaResponse = await callLambda(lambdaName, this.getRegion(), { action: 'dbMigrate', payload: {} })

  //   this.serverless.cli.log(`Migrator returned a response: ${JSON.stringify(lambdaResponse)}`)
  // }

//     let uploadfunction = this.serverless.service.functions.
//     this.serverless.cli.log('Triggering the upload Lambda function');
//     this.serverless.cli.commands.invoke --this.serverless.services.functions.upload
//   }
}

module.exports = TriggerLambda;
