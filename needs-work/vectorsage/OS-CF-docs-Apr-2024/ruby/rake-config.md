# Configuring Rake Tasks for deployed apps
For Cloud Foundry to automatically invoke a Rake task while a Ruby or Ruby on Rails app is deployed, you must do the following:

* Include the Rake task in your app.

* Configure the application start command using the `command` attribute in the application manifest.
Use the following example to invoke a Rake database migration task at application startup:

1. Create a file with the Rake task name and the extension `.rake`, and store it in the `lib/tasks` directory of your application.

2. Add the following code to your rake file:
```
namespace :cf do
desc "Only run on the first application instance"
task :on\_first\_instance do
instance\_index = JSON.parse(ENV["VCAP\_APPLICATION"])["instance\_index"] rescue nil
exit(0) unless instance\_index == 0
end
end
```
This Rake task limits an idempotent command to the first instance of a deployed application.

3. Add the task to the `manifest.yml` file with the `command` attribute, referencing the idempotent command `rake db:migrate` chained with a start command.
```
applications:

- name: my-rails-app
command: bundle exec rake cf:on\_first\_instance db:migrate && rails s -p $PORT
```