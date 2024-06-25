var vm = new Vue({
    el: '#app',
    data: {
        host: 'http://127.0.0.1:8000',
        user_id: '',
        orderRecords: [],
    },
    mounted: function () {
        // 获取cookie中的用户名
        this.username = getCookie('username');
        // 获取用户ID
        this.user_id = sessionStorage.user_id || localStorage.user_id;

        this.getOrderRecords();
    },
    methods: {
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
        getOrderRecords: function () {
            var url = this.host + '/userorder/';
            console.log("Request URL:", url);

            axios.get(url, {
                responseType: 'json',
                withCredentials: true,
            })
            .then(response => {
                this.orderRecords = response.data.records;
            })
            .catch(error => {
                status = error.response.status;
                if (status == 401 || status == 403) {
                    location.href = 'login.html?next=/user_center_order.html';
                } else {
                    // alert(error.response.data.detail);
                }
            });
        },
    }
});