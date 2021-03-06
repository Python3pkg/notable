// Configure require itself
require.config({
  baseUrl: '/js',
  shim: {
    underscore: {
      exports: '_'
    },
    backbone: {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    },
    bootstrap: {
      deps: ['jquery']
    }
  },
	paths: {
    ace: '../lib/ace/src-min/ace',
    backbone: '../lib/backbone',
    bootstrap: '../lib/bootstrap/js/bootstrap.min',
    jquery: '../lib/jquery',
    lib: '../lib',
    templates: '../templates',
    text: '../lib/plugins/require/text',
    underscore: '../lib/underscore'
	}
});

// The notable client side application
require(
	[
   'collections/notes',
   'views/table',
   'views/password',
   'views/search',
   'views/usage',
   'jquery',
   'underscore',
   'backbone',
   'bootstrap'
  ],
	function(NotesCollection, NotesTableView, PasswordModalView, SearchModalView, UsageModalView) {
    var notesView = new NotesTableView({
      collection: new NotesCollection(),
      el: $('#notes'),
      passwordModal: new PasswordModalView(),
      searchModal: new SearchModalView({
        el: $('#search'),
      }).render(),
      usageModal: new UsageModalView()
    });
	}
);
