// Configure require itself
require.config({
  baseUrl: '/static/js',
  shim: {
    underscore: {
      exports: '_'
    },
    backbone: {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  },
	paths: {
    backbone: '../lib/backbone',
    jquery: '../lib/jquery',
    lib: '../lib',
    templates: '../templates',
    underscore: '../lib/underscore',
    text: '../lib/plugins/require/text'
	}
});

// The notable client side application
require(
	[
   'collections/notes',
   'views/notesTable',
   'underscore',
   'backbone',
   'lib/plugins/bootstrap/tab'
  ],
	function(NotesCollection, NotesTableView) {
    var notesView = new NotesTableView({
      collection: new NotesCollection(),
      el: $('#notes')
    });
	}
);
