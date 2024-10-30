<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import ArgonPagination from "@/components/ArgonPagination.vue";
import ArgonPaginationItem from "@/components/ArgonPaginationItem.vue";
import { useRouter } from 'vue-router';
import { useStore } from 'vuex'; // 引入 Vuex store

const store = useStore(); // 获取 Vuex store
const currentPage = ref(1);
const itemsPerPage = ref(7);
const totalItems = ref(0);

// 定义收藏数组
const favorites = ref([]);

// 计算总页数
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value));

// 计算用户是否已登录
const isLoggedIn = computed(() => store.state.username !== '游客');

// 页面变化时的处理函数
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

// 获取收藏数据的函数
const fetchFavorites = () => {

  const username = store.state.username; // 从 Vuex 中获取用户名
  axios.get('http://localhost:5000/selectfavorites', {
      params: { username } // 将 username 作为查询参数传递
    })
    .then((response) => {
      console.log(response.data);

      if (response.data.code === 200) {
        favorites.value = response.data.data || []; // 确保 favorites 是数组
        totalItems.value = favorites.value.length;
      } else {
        console.error('获取收藏数据失败:', response.data.msg); // 使用 msg 获取失败信息
      }
    })
    .catch((error) => {
      console.error('请求失败:', error);
    });
};


// 组件挂载时获取收藏数据
onMounted(async () => {
  if (isLoggedIn.value) {
    await fetchFavorites();
  }
});

// 计算显示的收藏项（分页）
const displayedFavorites = computed(() => {
  if (!isLoggedIn.value || !Array.isArray(favorites.value)) return []; // 如果未登录，返回空数组
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return favorites.value.slice(start, end); // 返回当前页的收藏项
});

// 定义删除收藏项的函数
const deleteFavorite = async (dishname) => {
  if (!confirm(`确定要删除 ${dishname} 吗？`)) return;
  try {
    const formData = new FormData();
    formData.append("dishname",dishname);
    formData.append("username",store.state.username)
    const response = await axios.post('http://localhost:5000/delete_favorites', formData);
    if (response.status === 200) {
      favorites.value = favorites.value.filter(fav => fav[0] !== dishname);
      totalItems.value = favorites.value.length;
    } else {
      console.error('删除收藏失败:', response.data.message);
    }
  } catch (error) {
    console.error('删除收藏时出错:', error);
  }
};

// 路由实例
const router = useRouter();

// 定义跳转到食物详情的函数
const goToFoodDetail = (dishname) => {
  router.push({ name: 'food-detail', query: { foodName: dishname } });
};

</script>

<template>
  <div class="col-12">
    <h1 style="text-align: center;">我的收藏</h1>
    <div v-if="!isLoggedIn" class="alert alert-warning">
      请登录，才能查看收藏页面
    </div>
    <div v-else class="card">
      <div class="card-body px-0 pt-0 pb-2">
        <div class="table-responsive p-0">
          <table class="table align-items-center mb-0">
            <thead>
              <tr>
                <th>菜品名称</th>
                <th>分类</th>
                <th class="text-center">收藏时间</th>
                <th class="text-center"><i class="ni ni-settings-gear-65"></i></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(favorite, index) in displayedFavorites" :key="index">
                <td @click="goToFoodDetail(favorite[0])">{{ favorite[0] }}</td>
                <td>{{ favorite[1] }}</td>
                <td class="text-center">{{ favorite[2] }}</td>
                <td class="text-center">
                  <a href="javascript:;" @click="deleteFavorite(favorite[0])">删除</a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <argon-pagination class="pagination-centered">
      <argon-pagination-item :prev="true" @click="changePage(currentPage - 1)" />
      <argon-pagination-item v-for="page in totalPages" :key="page" :label="String(page)" :active="page === currentPage" @click="changePage(page)" />
      <argon-pagination-item :next="true" @click="changePage(currentPage + 1)" />
    </argon-pagination>
  </div>
</template>

<style scoped>
.pagination-centered {
  display: flex;
  justify-content: center;
  margin-top: 20px; /* 分页与上方内容的间距 */
}
</style>
