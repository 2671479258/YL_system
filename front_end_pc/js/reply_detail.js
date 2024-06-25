new Vue({
    el: '#app78',
    data: {
        doctorReply: {},
        healthRecord: {},
        loading: true
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
        const urlParams = new URLSearchParams(window.location.search);
        const recordId = urlParams.get('record_id');

        // 发送请求到后端获取医生回复信息
        axios.get(`http://127.0.0.1:8000/view_doctor_reply/${recordId}`)
            .then(response => {
                this.doctorReply = response.data.doctor_reply;
                this.healthRecord = response.data.health_record;

                this.loading = false;
            })
            .catch(error => {
                console.error('Error fetching doctor reply:', error);
                this.loading = false;
            });
    }
});