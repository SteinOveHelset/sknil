module.exports = function(grunt) {
    grunt.initConfig({
        sass: {
            dist: {
                options: {
                    style: 'compressed'
                },
                files: {
                    'static/styles/main.css': 'media/assets/styles/main.scss'
                }
            }
        },
        watch: {
            sass: {
                files: ['media/assets/styles/*.scss'],
                tasks: ['sass:dist']
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['sass:dist']);
};