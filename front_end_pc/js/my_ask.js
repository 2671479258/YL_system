new Vue({
    el: '#app666',
    data: {
        records: [], // 存储健康记录数据
        username: '' // 存储用户名
    },
    methods: {
        // 格式化日期时间
        formatDateTime: function(dateTimeString) {
            var dateTime = new Date(dateTimeString);
            var year = dateTime.getFullYear();
            var month = ("0" + (dateTime.getMonth() + 1)).slice(-2);
            var day = ("0" + dateTime.getDate()).slice(-2);
            var hours = ("0" + dateTime.getHours()).slice(-2);
            var minutes = ("0" + dateTime.getMinutes()).slice(-2);
            var seconds = ("0" + dateTime.getSeconds()).slice(-2);

            return year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" + seconds;
        }
    },
    mounted() {
        // 获取cookie中的用户名
        this.username = document.cookie.split('; ').find(row => row.startsWith('username=')).split('=')[1];

        // 发送GET请求获取健康记录数据，并传递用户名作为参数
        axios.get('http://127.0.0.1:8000/my_ask/', {
            params: {
                username: this.username // 将用户名作为参数传递
            }
        })
        .then(response => {
            // 格式化日期时间并更新数据
            this.records = response.data.records.map(record => {
                record.current_time = this.formatDateTime(record.current_time);
                return record;
            });
        })
        .catch(error => {
            console.error('Error fetching health records:', error);
        });
    }
});