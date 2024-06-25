new Vue({
    el: '#app9',
    data: {
        familyHistory: '0', // 默认值为有
        allergyHistory: '0' // 默认值为有
    },
    methods: {
        // 提交表单的方法
        submitForm: function () {
            var postData = {
                familyHistory: this.familyHistory,
                allergyHistory: this.allergyHistory
            };

            console.log(postData);
            // 使用 axios 发送 POST 请求
            axios.post('http://127.0.0.1:8000/edit_info/', postData, {
                withCredentials: true,
            })
            .then(function (response) {
                // 请求成功处理
        window.location.replace('http://127.0.0.1:8080/user_center_info.html');
                console.log(response.data);

            })
            .catch(function (error) {
                // 请求失败处理
                console.error(error);
            });
        }
    }
});