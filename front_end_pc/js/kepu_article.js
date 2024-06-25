var vm3 = new Vue({
    el: '#app3',
    data: {
        host: 'http://127.0.0.1:8000',
        user_id: '',  // 添加这一行，声明 user_id
        KpRecords: [],
    },

    mounted: function () {
        this.user_id = sessionStorage.user_id || localStorage.user_id;
        this.get_kepu_articles();
    },

    methods: {
        get_kepu_articles: function () {
            var url = this.host + '/kepu_article/';
            axios.get(url, {
                responseType: 'json',
                withCredentials: true,
            })
            .then(response => {
                this.KpRecords = response.data.KPrecords;
            })
            .catch(error => {
                status = error.response.status;
                if (status == 401 || status == 403) {
                    location.href = '127.0.0.1:8080/article.html';
                } else {
                    // alert(error.response.data.detail);
                }
            });
        }
    }
});