var app = angular.module('filesApp', ['angularFileUpload']);

app.config(function($httpProvider){
    // For CSRF token compatibility with Django
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.service('files', function($http, $upload){
    "use strict";
    return {
        get: function(){
            return $http.get('/files/');
        },
        upload: function (files) {
            if (files && files.length) {
                for (var i = 0; i < files.length; i++) {
                    var file = files[i];
                    $upload.upload({
                        url: '/files/',
//                        fields: {'username': $scope.username},
                        file: file
                    }).progress(function (evt) {
                        var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                        console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
                    }).success(function (data, status, headers, config) {
                        console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
                    });
                }
            }
        }
    }
});

app.controller("FilesCtrl", function($scope, files){
    "use strict";
    files.get().then(function(response){
        console.log(response.data);
        $scope.files = response.data.files;
    });

    $scope.$watch('upload_files', function () {
        files.upload($scope.upload_files);
    });

});
