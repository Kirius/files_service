'use strict';

angular.module('filesApp', ['filesApp.files'])

.config(function($httpProvider){
    // For CSRF token compatibility with Django
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});


