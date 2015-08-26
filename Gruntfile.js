// var mozjpeg = require('imagemin-mozjpeg');

module.exports = function(grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		sass: {
			dist: {
				files: [{
					expand: true,
					cwd: 'application/static/scss',
					src: ['style.scss'],
					dest: 'application/static/css',
					ext: '.css'
				}]
			}
		},
		cssmin: {
			options: {
				// aggressiveMerging: false,
				// advanced: false,
				noAdvanced: true,
				compatibility: "ie8"
			},
			combine: {
				files: {
					'application/static/css/style.min.css': [
						"application/static/css/normalize.min.css",
						"application/static/css/slick.css",
						"application/static/css/style.css",
					]
				}
			}
		},
		uglify: {
			js: {
				options: {
					// mangle: false,
					// compress: false,
					// beautify: true
				},
				files: {
					'application/static/js/main.min.js': [
						'application/static/js/lib/jquery.min.js',
						// 'application/static/js/lib/jquery.waypoints.min.js',
						// 'application/static/js/lib/skrollr.min.js',
						// 'application/static/js/lib/slick.min.js',
						'application/static/js/*.js'
					]
				}
			}
		},


		// responsive_images: {
		// 	first: {
		// 		options: {
		// 			engine: 'gm',
		// 			newFilesOnly: true,
		// 			upscale: false,
		// 			sizes: [{
		// 				name: 'tiny',
		// 				width: 640
		// 			}, {
		// 				name: 'small',
		// 				width: 1280
		// 			}, {
		// 				name: 'medium',
		// 				width: 2048,
		// 			}, {
		// 				name: 'large',
		// 				width: 4096,
		// 			}, {
		// 				name: 'original',
		// 				width: "100%",
		// 			}],
		// 		},
		// 		files: [{
		// 			expand: true,
		// 			src: ['**.{jpg,gif,png}'],
		// 			cwd: 'assets/pic/',
		// 			dest: 'assets/temp/'
		// 		}]

		// 	},
		// 	second: {
		// 		options: {
		// 			engine: 'gm',
		// 			newFilesOnly: true,
		// 			upscale: false,
		// 			sizes: [{
		// 				name: 'o',
		// 				width: '50%',
		// 				suffix: "@1x",
		// 			}, {
		// 				name: 'r',
		// 				width: '100%',
		// 				suffix: "@2x",
		// 			}],
		// 		},

		// 		files: [{
		// 			expand: true,
		// 			src: ['**.{jpg,gif,png}'],
		// 			cwd: 'assets/temp/',
		// 			dest: 'public_html/assets/pic/'
		// 		}]

		// 	}
		// },

		// imagemin: {
		// 	dynamic: { // Another target 
		// 		options: { // Target options 
		// 			optimizationLevel: 3,
		// 			svgoPlugins: [{
		// 				removeViewBox: false
		// 			}],
		// 			use: [mozjpeg()]
		// 		},
		// 		files: [{
		// 			expand: true, // Enable dynamic expansion 
		// 			cwd: 'public_html/assets/pic/', // Src matches are relative to this path 
		// 			src: ['**/*.{png,jpg,gif}'], // Actual patterns to match 
		// 			dest: 'public_html/assets/pic/' // Destination path prefix 
		// 		}]
		// 	}
		// },

		watch: {
			css: {
				files: ['application/static/**/*.scss'],
				tasks: ['sass', 'cssmin'] //
			},
			// html: {
			// 	files: ["html/**/*.html"],
			// 	tasks: ["includes", "htmlmin"]
			// },
			js: {
				files: 'application/static/**/*.js',
				tasks: ['uglify']
			},
			// img: {
			// 	files: 'assets/pic/**/*.jpg',
			// 	tasks: ['responsive_images:first', 'responsive_images:second'] //, 'imagemin']
			// }
		}
	});

	// grunt.loadNpmTasks('grunt-responsive-images');
	// grunt.loadNpmTasks('grunt-contrib-imagemin');

	grunt.loadNpmTasks('grunt-contrib-sass');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-uglify');

	grunt.loadNpmTasks('grunt-contrib-htmlmin');

	grunt.registerTask('default', ['watch']);
};