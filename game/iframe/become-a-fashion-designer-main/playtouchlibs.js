;(function(){
/*********************************************
				Array wait For Function
*********************************************/
	/*********************************************
				var
	*********************************************/
	var arrayWaitForFunction = function(){};
	arrayWaitForFunction.version = "1.0.0";
	arrayWaitForFunction.prototype.array = [];
	arrayWaitForFunction.prototype.id = 0;
	/*********************************************
				function
	*********************************************/
	arrayWaitForFunction.prototype.update = function(dt){
		for (var i = 0; i < this.array.length; i++) {
			this.array[i].time -= dt;
		};
		this.checkArrayEndOfTime();
	};

	arrayWaitForFunction.prototype.waitForFunction = function(timeToWait,callback,param){
		param = (Number(param) !== Number(param))?param:Number(param);
		this.array.push({
			time:timeToWait,
			callback:callback,
			param:param,
			id:this.id
		});
		return this.id++;
	};

	arrayWaitForFunction.prototype.checkArrayEndOfTime = function(){
		var toDestroy;
		for (var i = this.array.length - 1; i >= 0; i--) {
			if(this.array[i].time <= 0){
				toDestroy = this.array.splice(i,1)[0];
				break;
			}
		};

		if(typeof(toDestroy) != 'undefined'){
			c2_callFunction(toDestroy.callback,[toDestroy.param]);
			this.checkArrayEndOfTime();
		}
	};

	arrayWaitForFunction.prototype.clearArrayWait = function(){
		this.array = [];
	};

	arrayWaitForFunction.prototype.stopWaitById = function(id){
		for (var i = 0; i < this.array.length; i++) {
			if(this.array[i].id == id){
				this.array.splice(i,1);
				break;
			}
		};
	};

	arrayWaitForFunction.prototype.startWaitNowById = function(id){
		var toDestroy;
		for (var i = 0; i < this.array.length; i++) {
			if(this.array[i].id == id){
				toDestroy = this.array.splice(i,1)[0];
				break;
			}
		};
		if(typeof(toDestroy) != 'undefined'){
			c2_callFunction(toDestroy.callback,[toDestroy.param]);
		}
	};

/*********************************************
				Playtouch object
*********************************************/
	if(typeof(window.playtouch) != "object"){ window.playtouch = {};}
	playtouch.arrayWaitForFunction = new arrayWaitForFunction();
})();
