var vm6 = new Vue({
    el: '#app6',
    delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
    data: {
        host: host,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        page: 1, // 当前页数
        page_size: 5, // 每页数量
        count: 0,  // 总数量
        skus: [], // 数据
        query: '',  // 查询关键字
        cart_total_count: 0, // 购物车总数量
        cart: [], // 购物车数据
        searchkey:'',
        hot_skus:[] // 热销商品,


    },
    computed: {
        total_page: function(){  // 总页数
            // return Math.ceil(this.count/this.page_size);
            return this.count;
        },
        next: function(){  // 下一页
            if (this.page >= this.total_page) {
                return 0;
            } else {
                return this.page + 1;
            }
        },
        previous: function(){  // 上一页
            if (this.page <= 0 ) {
                return 0;
            } else {
                return this.page - 1;
            }
        },
        page_nums: function(){  // 页码
            // 分页页数显示计算
            // 1.如果总页数<=5
            // 2.如果当前页是前3页
            // 3.如果当前页是后3页,
            // 4.既不是前3页，也不是后3页
            var nums = [];
            if (this.total_page <= 5) {
                for (var i=1; i<=this.total_page; i++){
                    nums.push(i);
                }
            }
            else if (this.page <= 3) {
                nums = [1, 2, 3];
            }
            else if (this.total_page - this.page <= 2) {
                for (var i=this.total_page; i>this.total_page-5; i--) {
                    nums.push(i);
                }
            } else {
                for (var i=this.page-2; i<this.page+3; i++){
                    nums.push(i);
                }
            }
            return nums;
        }
    },


    mounted: function(){
         // 获取cookie中的用户名
    	this.username = getCookie('username');

        this.cat = this.get_query_string('cat');

        this.query = this.get_query_string('q');

        this.get_search_result();
        this.get_cart();
        this.get_hot_goods();
    },
    methods: {
        // 退出登录按钮
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
        // 获取url路径参数
        get_query_string: function(name){
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },
        // 请求查询结果
        get_search_result: function () {
    var url = this.host + '/search/';
    axios.get(url, {
        params: {
            q: this.query,
            page: this.page,
            page_size: this.page_size,

        },
        responseType: 'json',
        withCredentials: true,
    })
        .then(response => {
            this.skus = response.data.list;
            this.count = response.data.count;
            // 处理其他逻辑，如果有的话
            for(var i=0; i<this.skus.length; i++){
                        this.skus[i].url = '/goods/' + this.skus[i].id + ".html";
                    }
        })
        .catch(error => {
            console.log(error);
        });
},
         // 点击页数
        on_page: function(num){
            if (num != this.page){
                this.page = num;
                this.get_search_result();
            }
        },
        // 点击排序
        on_sort: function(ordering){
            if (ordering != this.ordering) {
                this.page = 1;
                this.ordering = ordering;
                this.get_skus();
            }
        },
        // 获取购物车数据
       get_cart(){
        let url = this.host + '/carts/simple/';
        axios.get(url, {
            responseType: 'json',
            withCredentials:true,
        })
            .then(response => {
                this.carts = response.data.cart_skus;
                this.cart_total_count = 0;
                for(let i=0;i<this.carts.length;i++){
                    if (this.carts[i].name.length>25){
                        this.carts[i].name = this.carts[i].name.substring(0, 25) + '...';
                    }
                    this.cart_total_count += this.carts[i].count;
                }
            })
            .catch(error => {
                console.log(error);
            })
    },
        // 获取热销商品数据
        get_hot_goods: function(){
            // 请求获取热销商品数据
            var url = this.host+'/hot/'+this.cat + '/'
            axios.get(url, {
                    responseType: 'json',
                    withCredentials: true
                })
                .then(response => {
                     this.hot_skus = response.data.hot_skus
                     for(let i=0; i<this.hot_skus.length; i++){
                        this.hot_skus[i].url = '/goods/' + this.skus[i].id + ".html";
                    }
                })
                .catch(error => {
                    console.log(error);
                })
        }
    }
});