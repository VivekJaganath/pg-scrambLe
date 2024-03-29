/*
Copyright (c) 2015 SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote 
products derived from this software without specific prior written 
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through 
the Horizon 2020 and 5G-PPP programmes. The authors would like to 
acknowledge the contributions of their colleagues of the SONATA 
partner consortium (www.sonata-nfv.eu).
*/

'use strict';

describe('GUI Integration test - Monitoring Server', function () {

  // load the controller's module
  beforeEach(module('SonataApp'));

  var MainCtrl, scope;

  // Initialize the controller and a mock scope


it('should returns status 200', inject(function($http,$httpBackend) {
  
  var $scope = {};

  
  /* Code Under Test */
  $http.get('http://sp.int3.sonata-nfv.eu:32001/functions')
    .success(function(data, status, headers, config) {
    	console.log(data);
      	$scope.valid = true;
    })
    .error(function(data, status, headers, config) {
    	console.log(data);
      $scope.valid = false;
  });
  

  $httpBackend.when('GET', 'http://sp.int3.sonata-nfv.eu:32001/functions').respond(200);
  $httpBackend.flush();

  expect($scope.valid).toBe(true);
  

}));


});