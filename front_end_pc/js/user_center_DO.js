var vm = new Vue({
    el: '#app',
    data: {
        host: 'http://127.0.0.1:8000',  // 请确保与后端API的地址匹配
        user_id: '',
        DORecords: [],
    },
    mounted: function () {
        // 获取cookie中的用户名
        this.username = getCookie('username');
        // 获取用户ID
        this.user_id = sessionStorage.user_id || localStorage.user_id;


        this.getDORecords();
    },
    methods: {
        getDORecords: function () {
            var url = this.host + '/show_doctor_order/';
            console.log("Request URL:", url);

            axios.get(url, {

                responseType: 'json',
                withCredentials: true,
            })
            .then(response => {
                this.DORecords = response.data.records;
            })
            .catch(error => {
                status = error.response.status;
                if (status == 401 || status == 403) {
                    location.href = 'login.html?next=/user_center_DO.html';
                } else {
                    // alert(error.response.data.detail);
                }
            });
        },
    }
});