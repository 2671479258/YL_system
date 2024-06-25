var vm = new Vue({
    el: '#app',
    data: {
        host: 'http://127.0.0.1:8000',  // 请确保与后端API的地址匹配
        user_id: '',
        tijianRecords: [],

    },
    mounted: function () {
        // // 获取cookie中的用户名
        // this.username = getCookie('username');
        // // 获取用户ID
        // this.user_id = sessionStorage.user_id || localStorage.user_id;


        this.getTijianRecords();
    },
    methods: {

        getTijianRecords: function () {
            var url = this.host + '/tijian/';
            console.log("Request URL:", url);

            axios.get(url, {

                responseType: 'json',
                withCredentials: true,
            })
            .then(response => {
                console.log(response.data.records)
                this.tijianRecords = response.data.records;
                this.username=response.data.username
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
    }
});