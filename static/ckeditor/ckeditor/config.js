/**
 * @license Copyright (c) 2003-2021, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
};

CKEDITOR.on('dialogDefinition', function(ev) {
  let dialogName       = ev.data.name;
  let dialogDefinition = ev.data.definition;
  console.log(ev);
  if (dialogName == 'image2') {
    dialogDefinition.onFocus = function() {
      /**
       * 'none' is no good for us - if is none - reset to 'center'
       * if it's already 'left','center', or 'right' - leave alone.
       */
      if (this.getContentElement('info', 'align')
          .getValue() === 'none') {
        this.getContentElement('info', 'align')
            .setValue('center');
      }
    };
  }
});