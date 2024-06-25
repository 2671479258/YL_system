var vm1 = new Vue({
    el: '#app1',
    data: {
        host: 'http://127.0.0.1:8000',
        user_id: '',  // 添加这一行，声明 user_id
        articleRecords: [],
    },

    mounted: function () {
        this.user_id = sessionStorage.user_id || localStorage.user_id;
        this.get_new_articles();
    },

    methods: {
        get_new_articles: function () {
            var url = this.host + '/new_article/';
            axios.get(url, {
                responseType: 'json',
                withCredentials: true,
            })
            .then(response => {
                this.articleRecords = response.data.records;
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