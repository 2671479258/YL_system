var vm = new Vue({
    el: '#app',
    data: {
        host: 'http://127.0.0.1:8000',  // 请确保与后端API的地址匹配
        user_id: '',
        tijianRecords: [],
        username: '',
        averageHeight: '',
        averageWeight: '',
        averageLefteye: '',
        averageRighteye: '',
        averageBloodPressure: '',
        averageHeartRate: '',
        averageBloodOxygen: ''


    },
    computed: {
        heightStatus: function () {
            if (this.averageHeight > 185) {
                return '偏高';
            } else if (this.averageHeight < 165) {
                return '偏低';
            } else {

                return '正常';
            }
        },
        weightStatus: function () {
            if (this.averageWeight > 80) {
                return '偏重';
            } else if (this.averageWeight < 60) {
                return '偏轻';
            } else {

                return '正常';
            }
        },
        lefteyeStatus: function () {
            if (this.averageLefteye > 1.0) {
                return '视力良好';
            } else if (this.averageLefteye > 0.5) {
                return '轻度近视';
            } else {
                return '严重近视';
            }
        },
        righteyeStatus: function () {
            if (this.averageRighteye > 1.0) {
                return '视力良好';
            } else if (this.averageRighteye > 0.5) {
                return '轻度近视';
            } else {
                return '严重近视';
            }
        },
        bloodPressureStatus: function () {
            if (this.averageBloodPressure > 120 || this.averageBloodPressure < 90) {
                return '血压异常';
            } else {
                return '血压正常';
            }
        },
        heartRateStatus: function () {
            if (this.averageHeartRate > 100 || this.averageHeartRate < 60) {
                return '心率异常';
            } else {
                return '心率正常';
            }
        },
        bloodOxygenStatus: function () {
            if (this.averageBloodOxygen > 95) {
                return '血氧饱和度良好';
            } else {
                return '血氧饱和度较低';
            }
        }
    },
    mounted: function () {
        // // 获取cookie中的用户名
        // this.username = getCookie('username');
        // // 获取用户ID
        // this.user_id = sessionStorage.user_id || localStorage.user_id;


        this.getTijianRecords();



    },
    methods: {
        // 退出登录按钮
        logoutfunc: function () {
            var url = this.host + '/logout/';
            axios.delete(url, {
                responseType: 'json',
                withCredentials:true,
            })
                .then(response => {
                    location.href = 'login.html';
                })
                .catch(error => {
                    console.log(error.response);
                })
        },

        getTijianRecords: function () {
            var url = this.host + '/show_tijian_avg/';
            console.log("Request URL:", url);

            axios.get(url, {

                responseType: 'json',
                withCredentials: true,
            })
            .then(response => {
                this.username = response.data.username;

        this.averageHeight = response.data.average_height;
        this.averageWeight = response.data.average_weight;
        this.averageLefteye = response.data.average_lefteye;
        this.averageRighteye = response.data.average_righteye;
        this.averageBloodPressure = response.data.average_blood_pressure;
        this.averageHeartRate = response.data.average_heart_rate;
        this.averageBloodOxygen = response.data.average_blood_oxygen;

            })
            .catch(error => {
                status = error.response.status;
                if (status == 401 || status == 403) {
                    location.href = 'login.html?next=/user_center_tijian.html';
                } else {
                    // alert(error.response.data.detail);
                }
            });
        },
       isHealthy: function() {
    return this.bloodPressureStatus === '血压正常' &&
           this.heartRateStatus === '心率正常' &&
           this.bloodOxygenStatus === '血氧饱和度良好' &&
           this.weightStatus === '体重正常';
},
unHealthyMessage: function() {
    var messages = [];
    if (this.bloodPressureStatus !== '血压正常') {
        messages.push('血压异常');
    }
    if (this.heartRateStatus !== '心率正常') {
        messages.push('心率异常');
    }
    if (this.weightStatus !== '正常') {
        messages.push('体重异常');
    }
    if (this.bloodOxygenStatus !== '血氧饱和度良好') {
        messages.push('血氧饱和度异常');
    }
    if (this.lefteyeStatus !== '视力良好' || this.righteyeStatus !== '视力良好') {
        messages.push('视力不佳');
    }
    return messages.length > 0 ? messages : ['无异常'];
}
    }
});