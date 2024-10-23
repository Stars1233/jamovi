'use strict';

const $ = require('jquery');
const GridOptionControl = require('./gridoptioncontrol');
const FormatDef = require('./formatdef');
const _focusLoop = require('../common/focusloop');

const GridCombobox = function(params) {

    GridOptionControl.extendTo(this, params);

    this.registerOptionProperty("options");
    this.registerSimpleProperty("format", FormatDef.string);

    this.$label = null;

    this.getOptionsProperty = function() {
        let options = this.getPropertyValue('options');
        if (options === null)
            options = [];

        if (options.length > 0) {
            if (typeof options[0] === 'string') {
                let newOptions = [];
                for (let i = 0; i < options.length; i++)
                    newOptions[i] = { title: this.translate(options[i]), name: options[i] };
                this.setPropertyValue('options', newOptions);
                options = newOptions;
            }
        }

        return options;
    };

    this.onRenderToGrid = function(grid, row, column) {

        let label = this.getPropertyValue('label');
        if (label === null)
            label = '';

        label = this.translate(label);
        let id = _focusLoop.getNextAriaElementId('ctrl');

        let columnUsed = 0;
        let cell = null;
        if (label !== "") {
            this.$label = $(`<label for="${id}" class="silky-option-combo-label silky-control-margin-${this.getPropertyValue("margin")}" style="display: inline; white-space: nowrap;" >${label}</label>`);
            cell = grid.addCell(column, row, this.$label);
            cell.setAlignment("left", "center");
            columnUsed += 1;
        }

        let options = this.getOptionsProperty();

        let t = `<select id="${id}" class="silky-option-input silky-option-combo-input silky-control-margin-${this.getPropertyValue("margin")}">`;
        for (let i = 0; i < options.length; i++)
            t += '<option>' + this.translate(options[i].title) + '</option>';
        t += '</select>';

        let self = this;
        this.$input = $(t);
        this.updateDisplayValue();
        this.$input.change(function(event) {
            let opts = self.getOptionsProperty();
            let select = self.$input[0];
            let option = opts[select.selectedIndex];
            let value = option.name;
            self.setValue(value);
        });

        let spans = { rows: 1, columns: 1 };
        let vAlign = 'top';
        if (columnUsed === 0 && this.isPropertyDefined('cell')) {
            spans = { rows: 1, columns: 2 };
            vAlign = 'center';
        }
        
        cell = grid.addCell(column + columnUsed, row, this.$input, { spans, vAlign });
        cell.setAlignment("left", "center");

        columnUsed += 1;

        return { height: 1, width: columnUsed };
    };

    this.onOptionValueChanged = function(key, data) {
        if (this.$input)
            this.updateDisplayValue();
    };

    this.updateDisplayValue = function() {
        let select = this.$input[0];
        let value = this.getSourceValue();
        let options = this.getOptionsProperty();
        let index = -1;
        for (let i = 0; i < options.length; i++) {
            if (options[i].name === value) {
                index = i;
                break;
            }
        }
        if (index !== -1)
            select.selectedIndex = index;
    };

    this.updateOptionsList = function() {
        if ( ! this.$input) 
            return;

        let options = this.getOptionsProperty();

        let html = '';
        for (let i = 0; i < options.length; i++)
            html += '<option>' + this.translate(options[i].title) + '</option>';

        this.$input.empty();
        this.$input.html(html);

        this.updateDisplayValue();
    };

    this._override('onPropertyChanged', (baseFunction, name) => {
        if (baseFunction !== null)
            baseFunction.call(this, name);

        if (name === 'options') {
            this.updateOptionsList();
        }
        else if (name === 'enable') {
            let enabled = this.getPropertyValue(name);
            this.$input.prop('disabled', enabled === false);
            if (this.$label !== null) {
                if (enabled)
                    this.$label.removeClass('disabled-text');
                else
                    this.$label.addClass('disabled-text');
            }
        }
    });
};

module.exports = GridCombobox;
