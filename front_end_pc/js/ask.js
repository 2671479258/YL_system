var vm = new Vue({
    el: '#app4',
    data: {
        formData: {
            // 自测的一些身体数据
            bloodPressure: '',
            bodyTemperature: '',
            heartRate: '',
            bloodSugar: '',
            bodyWeight: '',
            bodyHeight: '',
            bloodOxygen: '',
            // 身体状况
            noSymptoms: false,
            headache: false,
            fever: false,
            cough: false,
            chestPain: false,
            abdominalPain: false,
            nausea: false,
            vomiting: false,
            otherSymptoms: '',
            // 其他身体状况
            balancedDiet: false,
            unbalancedDiet: false,
            goodSleepQuality: false,
            poorSleepQuality: false,
            sufficientExerciseDuration: false,
            lackOfExercise: false,
            noAnxiety: false,
            anxiety: false,
            noMedication: false,
            medication: false,
            medicationDetails: '',
            noOtherPhysicalConditions: false,
            otherPhysicalConditions: false,
            otherPhysicalConditionsDetails: ''
        }
    },
    methods: {
        submitForm: function() {
            // 获取cookie中的username
            const username = this.getCookie('username');
            console.log(username);

            // 收集表单数据
            const formData = this.formData;

            // 合并username到表单数据中
            formData.username = username;

            axios.post('http://127.0.0.1:8000/doctor_ask/', formData)
                .then(function(response) {
                    console.log(response.data); // 打印后端返回的数据
                    alert('表单提交成功！');
                })
                .catch(function(error) {
                    console.error(error); // 打印错误信息
                    alert('表单提交失败，请稍后重试。');
                    window.location.href = 'http://example.com/success-page';
                });
        },
        getCookie: function(name) {
            const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
            return cookieValue ? cookieValue.pop() : '';
        }
    }
});