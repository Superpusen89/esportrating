app.service('daoCountries', function ($http, REST) {

    this.getAll = function (successCallback, errorCallback) {
        $http.get(REST.path + 'countries').success(function (result) {
            if (typeof (successCallback) === 'function') {
                successCallback(result);
            }
        }).error(function () {
            if (typeof (errorCallback) === 'function') {
                errorCallback();
            }
        });
    };
});