//
// Copyright (C) 2016 Jonathon Love
//

'use strict';

const $ = require('jquery');
const Backbone = require('backbone');
Backbone.$ = $;

const host = require('../host');
const Notify = require('../notification');

const PageSideload = Backbone.View.extend({
    className: 'PageSideload',
    initialize() {

        this.$el.addClass('jmv-store-page-sideload');
        this.$el.attr('role', 'tabpanel');
        this.$body = $('<div class="jmv-store-body"></div>').appendTo(this.$el);
        this.$drop = $('<button class="jmv-store-page-installed-drop" tabindex="-1"><span class="mif-file-upload"></span></button>')
            .appendTo(this.$body)
            .on('click', event => this._dropClicked());
    },
    async _dropClicked(event) {
        if (host.isElectron) {

            let filters = [ { name: _('jamovi modules'), extensions: ['jmo']} ];
            let result = await host.showOpenDialog({ filters });

            if ( ! result.cancelled) {
                const path = result.paths[0];
                try {
                    await this.model.install(path);
                    this._installSuccess();
                }
                catch (e) {
                    this._installFailure(e);
                }
            }

            this.$drop.focus();
        }
    },
    _installSuccess() {
        this.trigger('notification', new Notify({
            title: _('Module installed successfully'),
            message: '',
            duration: 3000,
            type: 'success'
        }));
        this.trigger('close');
    },
    _installFailure(error) {
        this.trigger('notification', new Notify({
            message: error.message,
            title: _('Unable to install module'),
            duration: 4000,
            type: 'error'
        }));
    },
});

module.exports = PageSideload;
