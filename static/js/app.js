var app = angular.module('filesApp', ['angularFileUpload']);

app.config(function($httpProvider){
    // For CSRF token compatibility with Django
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.filter('filesize', function(){
    "use strict";
    var units = ['bytes', 'KB', 'MB', 'GB'];

    return function(bytes, precision) {
        if (isNaN( parseFloat(bytes)) || !isFinite(bytes)){
            return '?';
        }
        var unit = 0;
        while ( bytes >= 1024 ) {
            bytes /= 1024;
            unit ++;
        }
        return bytes.toFixed(+precision) + ' ' + units[unit];
    };
});

app.filter('pct', function(){
    "use strict";
    return function(num) {
       return num + '%';
    };
});

app.service('files', function($http, $upload){
    "use strict";
    return {
        get: function(){
            return $http.get('/files/');
        },
        upload: function (file) {
            return $upload.upload({
                url: '/files/',
                file: file
            })
        }
    }
});

app.controller("FilesCtrl", function($scope, files){
    "use strict";

    function findInArrayByProperty(array, name, value){
        for (var i = 0; i < array.length; i++){
            if (array[i][name] === value){
                return array[i];
            }
        }
    }

    files.get().then(
        function(response){
            $scope.files = response.data.files;
        },
        function(){
            // Notify unknown error
        }
    );

    $scope.$watch('upload_files', function () {
        if (!$scope.upload_files) {
            return;
        }
        if ($scope.upload_files.length > 5){
            $scope.too_many_files = true;
            $scope.upload_files = undefined;
            return;
        }
        $scope.too_many_files = false;
        angular.forEach($scope.upload_files, function(file){
            file.progress = 0;
            if (findInArrayByProperty($scope.files, 'name', file.name)){
                file.error = 'You already have a file with such name';
                return;
            }
            files.upload(file)
                .progress(function(evt) {
                    file.progress = parseInt(100.0 * evt.loaded / evt.total);
                })
                .success(function(data) {
                    file.msg = data.msg;
                    $scope.files.unshift(data.file);
                })
                .error(function(data){
                    file.error = data.error || 'Unknown error!';
                });
        });
    });

});
