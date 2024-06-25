var vm = new Vue({
    el: '#app',
    data: {
        host: 'http://127.0.0.1:8000',
        doctors: [],
        doctorsRows: [],  // 用于存放分行后的医生列表
    },
    mounted: function () {
        this.getDoctorData();
    },
    methods: {
        getDoctorData: function () {
            var url = this.host + '/doctor_show/';
            console.log("Request URL:", url);

            axios.get(url, {
                responseType: 'json',
                withCredentials: true,
            })
            .then(response => {
                this.doctors = response.data.records;
                // 在这里调用分行函数
                this.splitDoctorsIntoRows();
            })
            .catch(error => {
                console.error(error);
            });
        },
        // 新增的分行函数
        splitDoctorsIntoRows: function () {
            const doctorsPerPage = 4;
            const rows = [];
            for (let i = 0; i < this.doctors.length; i += doctorsPerPage) {
                rows.push(this.doctors.slice(i, i + doctorsPerPage));
            }
            this.doctorsRows = rows;
        },
    }
});