/*global gettext, interpolate, ngettext*/
'use strict';
{
    // Main JavaScript utility functions for Django Admin
    const $ = django.jQuery;
    let lastChecked;

    // Quick element creation
    // quickElement(tagType, parentElement [, textInChildNode, attribute, attributeValue ...]);
    function quickElement() {
        const obj = document.createElement(arguments[0]);
        if (arguments[2]) {
            const textNode = document.createTextNode(arguments[2]);
            obj.appendChild(textNode);
        }
        const len = arguments.length;
        for (let i = 3; i < len; i += 2) {
            obj.setAttribute(arguments[i], arguments[i + 1]);
        }
        arguments[1].appendChild(obj);
        return obj;
    }

    // Remove all child nodes from an element
    function removeChildren(element) {
        while (element.hasChildNodes()) {
            element.removeChild(element.lastChild);
        }
    }

    // Add an event listener to an element
    function addEvent(element, eventName, handler) {
        element.addEventListener(eventName, handler);
    }

    // Remove an event listener from an element
    function removeEvent(element, eventName, handler) {
        element.removeEventListener(eventName, handler);
    }

    // Get the value of a cookie
    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }

    // Set a cookie
    function setCookie(name, value, expires, path, domain, secure) {
        document.cookie = name + '=' + value +
            (expires ? '; expires=' + expires.toUTCString() : '') +
            (path ? '; path=' + path : '') +
            (domain ? '; domain=' + domain : '') +
            (secure ? '; secure' : '');
    }

    // Delete a cookie
    function deleteCookie(name, path, domain) {
        setCookie(name, '', new Date(0), path, domain);
    }

    // Format a date
    function formatDate(date) {
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        return year + '-' + month + '-' + day;
    }

    // Format a time
    function formatTime(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const seconds = date.getSeconds().toString().padStart(2, '0');
        return hours + ':' + minutes + ':' + seconds;
    }

    // Format a datetime
    function formatDateTime(date) {
        return formatDate(date) + ' ' + formatTime(date);
    }

    // Get the current date
    function getCurrentDate() {
        return new Date();
    }

    // Get the current time
    function getCurrentTime() {
        return new Date();
    }

    // Get the current datetime
    function getCurrentDateTime() {
        return new Date();
    }

    // Add days to a date
    function addDays(date, days) {
        const result = new Date(date);
        result.setDate(result.getDate() + days);
        return result;
    }

    // Add months to a date
    function addMonths(date, months) {
        const result = new Date(date);
        result.setMonth(result.getMonth() + months);
        return result;
    }

    // Add years to a date
    function addYears(date, years) {
        const result = new Date(date);
        result.setFullYear(result.getFullYear() + years);
        return result;
    }

    // Check if a date is valid
    function isValidDate(date) {
        return date instanceof Date && !isNaN(date);
    }

    // Check if a string is a valid date
    function isValidDateString(dateString) {
        const date = new Date(dateString);
        return isValidDate(date);
    }

    // Check if a string is a valid time
    function isValidTimeString(timeString) {
        const timeRegex = /^([01]?[0-9]|2[0-3]):[0-5][0-9](:[0-5][0-9])?$/;
        return timeRegex.test(timeString);
    }

    // Check if a string is a valid datetime
    function isValidDateTimeString(dateTimeString) {
        const dateTime = new Date(dateTimeString);
        return isValidDate(dateTime);
    }

    // Parse a date string
    function parseDate(dateString) {
        const date = new Date(dateString);
        return isValidDate(date) ? date : null;
    }

    // Parse a time string
    function parseTime(timeString) {
        if (!isValidTimeString(timeString)) {
            return null;
        }
        const [hours, minutes, seconds = '00'] = timeString.split(':');
        const date = new Date();
        date.setHours(parseInt(hours, 10));
        date.setMinutes(parseInt(minutes, 10));
        date.setSeconds(parseInt(seconds, 10));
        return date;
    }

    // Parse a datetime string
    function parseDateTime(dateTimeString) {
        return parseDate(dateTimeString);
    }

    // Export functions
    window.django = {
        jQuery: $,
        quickElement: quickElement,
        removeChildren: removeChildren,
        addEvent: addEvent,
        removeEvent: removeEvent,
        getCookie: getCookie,
        setCookie: setCookie,
        deleteCookie: deleteCookie,
        formatDate: formatDate,
        formatTime: formatTime,
        formatDateTime: formatDateTime,
        getCurrentDate: getCurrentDate,
        getCurrentTime: getCurrentTime,
        getCurrentDateTime: getCurrentDateTime,
        addDays: addDays,
        addMonths: addMonths,
        addYears: addYears,
        isValidDate: isValidDate,
        isValidDateString: isValidDateString,
        isValidTimeString: isValidTimeString,
        isValidDateTimeString: isValidDateTimeString,
        parseDate: parseDate,
        parseTime: parseTime,
        parseDateTime: parseDateTime
    };
}
