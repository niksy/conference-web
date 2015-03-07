/* jshint node:true */

module.exports = function ( grunt ) {

    grunt.initConfig({

        sass: {
            dist: {
                options: {
                    sourcemap: 'none',
                    style: 'expanded',
                    precision: 5
                },
                files: {
                    'output/_index.css': 'assets/style/index.scss'
                }
            }
        },

        cssmin: {
            dist: {
                options: {
                    keepSpecialComments: 0,
                    restructuring: false
                },
                files: {
                    'output/index.css': [
                        'node_modules/normalize.css/normalize.css',
                        'node_modules/rationalize.css/dist/rationalize.css',
                        'output/_index.css'
                    ]
                }
            }
        },

        watch: {
            sass: {
                files: ['assets/style/**/*.scss'],
                tasks: ['sass']
            },
            cssmin: {
                files: ['output/_index.css'],
                tasks: ['cssmin']
            }
        },

        connect: {
            dev: {
                options: {
                    open: true
                }
            }
        },

        concurrent: {
            main: {
                options: {
                    logConcurrentOutput: true
                },
                tasks: ['watch:sass', 'watch:cssmin', 'connect:dev:keepalive']
            }
        }

    });

    require('load-grunt-tasks')(grunt);

    grunt.registerTask('default', ['sass','cssmin']);
    grunt.registerTask('dev', ['default','concurrent']);

};
