'use strict';

angular.module('filesApp.files', ['angularFileUpload', 'toaster'])

.filter('filesize', function(){
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
})

.filter('pct', function(){
    return function(num) {
       return num + '%';
    };
})

.filter('date', function(){
    return function(iso_string) {
       var date = new Date(iso_string);
        return date.toString();
    };
})

.service('files', function($http, $upload){
    return {
        get: function(){
            return $http.get('/files');
        },
        upload: function (file) {
            return $upload.upload({
                url: '/files',
                file: file
            })
        },
        delete: function(id){
            return $http.delete('/files/' + id)
        }
    }
})

.controller("FilesCtrl", function($scope, files, toaster){

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
            toaster.pop('error', 'Error', 'Unknown error during fetching files')
        }
    );

    $scope.$watch('upload_files', function () {
        $scope.hide_upload_files = false;
        if (!$scope.upload_files) {
            return;
        }
        if ($scope.upload_files.length > 5){
            toaster.pop('error', 'Error', 'You can upload at most 5 files at a time');
            $scope.hide_upload_files = true;
            return;
        }
        angular.forEach($scope.upload_files, function(file){
            file.progress = 0;
            if (findInArrayByProperty($scope.files, 'name', file.name)){
                file.error = 'You already have a file with such name';
                return;
            }
            files.upload(file)
                .progress(function(evt) {
                    var pct = Math.min(parseInt(100.0 * evt.loaded / evt.total), 99);
                    file.progress = pct;
                })
                .success(function(data) {
                    file.progress = 100;
                    file.msg = data.msg;
                    $scope.files.unshift(data.file);
                })
                .error(function(data){
                    file.error = data.error || 'Unknown error!';
                });
        });
    });

    $scope.deleteFile = function(file, idx){
        $scope.upload_files = undefined;
        if (!confirm("Do you want to delete '" + file.name + "' file?")) {
            return;
        }
        files.delete(file.id).then(
            function(){
                $scope.files.splice(idx, 1);
                toaster.pop('success', 'Success', 'File ' + file.name + ' was deleted');
            },
            function(response){
                var error = response.data.error || 'Unknown error';
                toaster.pop('error', 'Error', error);
            }
        );
    }
});
