/*global gettext, interpolate, ngettext, Actions*/
'use strict';
{
    // Show elements that match the selector
    function show(selector) {
        document.querySelectorAll(selector).forEach(function(el) {
            el.classList.remove('hidden');
        });
    }

    // Hide elements that match the selector
    function hide(selector) {
        document.querySelectorAll(selector).forEach(function(el) {
            el.classList.add('hidden');
        });
    }

    // Show question for selected items
    function showQuestion(options) {
        show(options.acrossClears);
        hide(options.acrossQuestions);
        hide(options.allContainer);
    }

    // Show clear button for selected items
    function showClear(options) {
        show(options.acrossQuestions);
        hide(options.acrossClears);
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
        show(options.allContainer);
        hide(options.counterContainer);
    }

    // Reset selection
    function reset(options) {
        hide(options.acrossQuestions);
        hide(options.acrossClears);
        hide(options.allContainer);
        show(options.counterContainer);
    }

    // Clear selection across all pages
    function clearAcross(options) {
        reset(options);
        const acrossInputs = document.querySelectorAll(options.acrossInput);
        acrossInputs.forEach(function(acrossInput) {
            acrossInput.value = 0;
        });
        document.querySelector(options.actionContainer).classList.remove(options.selectedClass);
    }

    // Checkbox checker
    function checker(actionCheckboxes, options, checked) {
        if (checked) {
            showQuestion(options);
        } else {
            reset(options);
        }
        actionCheckboxes.forEach(function(el) {
            el.checked = checked;
            el.closest('tr').classList.toggle('selected', checked);
        });
    }

    // Update counter
    function updateCounter(actionCheckboxes, options) {
        const sel = Array.from(actionCheckboxes).filter(function(el) {
            return el.checked;
        }).length;
        const counter = document.querySelector(options.counterContainer);
        // data-actions-icnt is defined in the generated HTML
        // and contains the total amount of objects in the queryset
        const actions_icnt = document.querySelector('[data-actions-icnt]').dataset.actionsIcnt;
        counter.textContent = interpolate(
            ngettext('%(sel)s of %(cnt)s selected', '%(sel)s of %(cnt)s selected', sel), {
                sel: sel,
                cnt: actions_icnt
            }, true);
        const allToggle = document.getElementById(options.allToggleId);
        updateAllToggle(sel, actionCheckboxes.length, allToggle, options);
    }

    // Update all toggle
    function updateAllToggle(sel, tot, allToggle, options) {
        if (allToggle) {
            // If there are none selected, uncheck the "all" toggle
            if (sel === 0) {
                allToggle.checked = false;
                allToggle.indeterminate = false;
            }
            // If not all are selected, set the "all" toggle to indeterminate
            else if (sel !== tot) {
                allToggle.checked = false;
                allToggle.indeterminate = true;
            }
            // If all are selected, check the "all" toggle
            else {
                allToggle.checked = true;
                allToggle.indeterminate = false;
            }
        }
    }

    // Initialize action checkboxes
    const actionsEls = document.querySelectorAll('tr input.action-select');
    if (actionsEls.length > 0) {
        const actionsBox = Array.from(actionsEls);
        let counter_el = document.querySelector('.actions .counter');
        const allToggle = document.getElementById('action-toggle');
        const acrossInputs = document.querySelectorAll('select[name="action"]');
        const options = {
            actionContainer: "div.actions",
            counterContainer: "span.action-counter",
            allContainer: "div.actions span.all",
            acrossInput: "div.actions input.select-across",
            acrossQuestions: "div.actions span.question",
            acrossClears: "div.actions span.clear",
            allToggleId: "action-toggle",
            selectedClass: "selected"
        };

        // List of available actions
        const actions_icnt = document.querySelector('[data-actions-icnt]').dataset.actionsIcnt;
        if (actions_icnt > 0) {
            show(options.counterContainer);
        } else {
            hide(options.counterContainer);
        }

        // Update counter when checkboxes are clicked
        actionsBox.forEach(function(el) {
            el.addEventListener('change', function(e) {
                const target = e.target;
                if (target.classList.contains('action-select')) {
                    target.closest('tr').classList.toggle('selected', target.checked);
                    updateCounter(actionsBox, options);
                }
            });
        });

        // Update counter when "all" toggle is clicked
        if (allToggle) {
            allToggle.addEventListener('click', function() {
                checker(actionsBox, options, this.checked);
                updateCounter(actionsBox, options);
            });
        }

        // Clear selection when "clear" button is clicked
        document.querySelector(options.acrossClears).addEventListener('click', function() {
            clearAcross(options);
        });

        // Show question when "select all" is clicked
        document.querySelector(options.acrossQuestions).addEventListener('click', function() {
            showQuestion(options);
        });

        // Update counter on page load
        updateCounter(actionsBox, options);
    }

    // Default settings for actions
    const defaults = {
        actionContainer: "div.actions",
        counterContainer: "span.action-counter",
        allContainer: "div.actions span.all",
        acrossInput: "div.actions input.select-across",
        acrossQuestions: "div.actions span.question",
        acrossClears: "div.actions span.clear",
        allToggleId: "action-toggle",
        selectedClass: "selected"
    };

    // Main function that manages bulk actions
    window.Actions = function(actionCheckboxes, options) {
        options = Object.assign({}, defaults, options);
        let list_editable_changed = false;
        let lastChecked = null;
        let shiftPressed = false;

        // Monitor Shift key
        document.addEventListener('keydown', (event) => {
            shiftPressed = event.shiftKey;
        });

        document.addEventListener('keyup', (event) => {
            shiftPressed = event.shiftKey;
        });

        // Event for select/deselect all
        document.getElementById(options.allToggleId).addEventListener('click', function(event) {
            checker(actionCheckboxes, options, this.checked);
            updateCounter(actionCheckboxes, options);
        });

        // Event for confirming bulk selection
        document.querySelectorAll(options.acrossQuestions + " a").forEach(function(el) {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                const acrossInputs = document.querySelectorAll(options.acrossInput);
                acrossInputs.forEach(function(acrossInput) {
                    acrossInput.value = 1;
                });
                showClear(options);
            });
        });

        // Event for clearing bulk selection
        document.querySelectorAll(options.acrossClears + " a").forEach(function(el) {
            el.addEventListener('click', function(event) {
                event.preventDefault();
                document.getElementById(options.allToggleId).checked = false;
                clearAcross(options);
                checker(actionCheckboxes, options, false);
                updateCounter(actionCheckboxes, options);
            });
        });

        // Return checkboxes affected by Shift selection
        function affectedCheckboxes(target, withModifier) {
            const multiSelect = (lastChecked && withModifier && lastChecked !== target);
            if (!multiSelect) {
                return [target];
            }
            const checkboxes = Array.from(actionCheckboxes);
            const targetIndex = checkboxes.findIndex(el => el === target);
            const lastCheckedIndex = checkboxes.findIndex(el => el === lastChecked);
            const startIndex = Math.min(targetIndex, lastCheckedIndex);
            const endIndex = Math.max(targetIndex, lastCheckedIndex);
            const filtered = checkboxes.filter((el, index) => (startIndex <= index) && (index <= endIndex));
            return filtered;
        };

        // Event for checkbox changes
        Array.from(document.getElementById('result_list').tBodies).forEach(function(el) {
            el.addEventListener('change', function(event) {
                const target = event.target;
                if (target.classList.contains('action-select')) {
                    const checkboxes = affectedCheckboxes(target, shiftPressed);
                    checker(checkboxes, options, target.checked);
                    updateCounter(actionCheckboxes, options);
                    lastChecked = target;
                } else {
                    list_editable_changed = true;
                }
            });
        });

        // Event for index button
        document.querySelector('#changelist-form button[name=index]').addEventListener('click', function(event) {
            if (list_editable_changed) {
                const confirmed = confirm(gettext("Você tem alterações não salvas em campos editáveis individuais. Se você executar uma ação, suas alterações não salvas serão perdidas."));
                if (!confirmed) {
                    event.preventDefault();
                }
            }
        });

        // Event for save button
        const el = document.querySelector('#changelist-form input[name=_save]');
        // The button does not exist if there are no editable fields
        if (el) {
            el.addEventListener('click', function(event) {
                if (document.querySelector('[name=action]').value) {
                    const text = list_editable_changed
                        ? gettext("Você selecionou uma ação, mas ainda não salvou suas alterações em campos individuais. Clique em OK para salvar. Você precisará executar a ação novamente.")
                        : gettext("Você selecionou uma ação e não fez alterações em campos individuais. Você provavelmente está procurando o botão Ir em vez do botão Salvar.");
                    if (!confirm(text)) {
                        event.preventDefault();
                    }
                }
            });
        }
        // Synchronize counter when navigating to a page, such as through the back button
        window.addEventListener('pageshow', (event) => updateCounter(actionCheckboxes, options));
    };

    // Call fn when the DOM is loaded and ready
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    // Initialize actions when the DOM is ready
    ready(function() {
        const actionsEls = document.querySelectorAll('tr input.action-select');
        if (actionsEls.length > 0) {
            Actions(actionsEls);
        }
    });
}
