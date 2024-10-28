<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import Mock from 'mockjs';
import ArgonPagination from "@/components/ArgonPagination.vue";
import ArgonPaginationItem from "@/components/ArgonPaginationItem.vue";
import { useRoute } from 'vue-router';

// Mock.js for simulating the API responses
Mock.mock('http://localhost:5000/selectfavorites', 'get', {
  status: 200,
  message: '成功获取收藏数据',
  data: [
    { dishname: '宫保鸡丁', category: '甜口', date: '23/04/18' },
    { dishname: '鱼香肉丝', category: '甜口', date: '23/04/19' },
    { dishname: '清蒸排骨', category: '清淡', date: '23/04/19' },
  ],
});

Mock.mock('http://localhost:5000/delete_favorites', 'post', (options) => {
  const { dishname } = JSON.parse(options.body);
  return {
    status: 200,
    message: `成功删除 ${dishname} 收藏`,
  };
});

// Define current page and items per page for pagination
const currentPage = ref(1);
const itemsPerPage = ref(7);
const totalItems = ref(0);

// Calculate total pages
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value));

// Change page
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

// Define favorites array
const favorites = ref([]);

// Fetch favorites data
const fetchFavorites = async () => {
  try {
    const response = await axios.get('http://localhost:5000/selectfavorites');
    if (response.status === 200) {
      favorites.value = response.data.data;
      totalItems.value = favorites.value.length; // Update total items directly
    } else {
      console.error('获取收藏数据失败:', response.data.message);
    }
  } catch (error) {
    console.error('请求失败:', error);
  }
};

// Delete favorite
const deleteFavorite = async (dishname) => {
  if (!confirm(`确定要删除 ${dishname} 吗？`)) return;
  try {
    const payload = { dishname };
    const response = await axios.post('http://localhost:5000/delete_favorites', payload);
    if (response.status === 200) {
      favorites.value = favorites.value.filter(fav => fav.dishname !== dishname);
      totalItems.value = favorites.value.length; // Update total items after deletion
    } else {
      console.error('删除收藏失败:', response.data.message);
    }
  } catch (error) {
    console.error('删除收藏时出错:', error);
  }
};

// Define route instance to get food name and timestamp
const route = useRoute();
const foodName = ref('');
const timestamp = ref('');

// Get food name and timestamp from route parameters on mount
onMounted(async () => {
  // Fetch existing favorites
  await fetchFavorites();
  
  // Get food name and timestamp from route parameters
  foodName.value = route.query.foodName || '未知食物';
  timestamp.value = route.query.timestamp || new Date().toLocaleString();
  
  // 添加新的收藏项到 favorites 数组，如果该项尚未存在
  const newFavorite = {
    dishname: foodName.value,
    category: '未知分类', // 根据实际情况更新分类
    date: timestamp.value
  };
  
  // 只在新收藏项的名称不在 favorites 列表中时添加
  if (!favorites.value.some(fav => fav.dishname === newFavorite.dishname)) {
    favorites.value.unshift(newFavorite);
    totalItems.value = favorites.value.length; // 更新总数
  }
});

// Compute the favorites to display based on pagination
const displayedFavorites = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return favorites.value.slice(start, end);
});
</script>

<template>
  <div class="col-12">
    <h1 style="text-align: center;">我的收藏</h1>

    <div class="card">
      <div class="card-body px-0 pt-0 pb-2">
        <div class="table-responsive p-0">
          <table class="table align-items-center mb-0">
            <thead>
              <tr>
                <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">菜品名称</th>
                <th class="text-uppercase text-secondary text-xxs font-weight-bolder opacity-7 ps-2">分类</th>
                <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7">收藏时间</th>
                <th class="text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"><i class="ni ni-settings-gear-65"></i></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(favorite, index) in displayedFavorites" :key="index">
                <td>
                  <div class="d-flex px-2 py-1">
                    <div class="d-flex flex-column justify-content-center">
                      <h6 class="mb-0 text-sm">{{ favorite.dishname }}</h6>
                    </div>
                  </div>
                </td>
                <td>
                  <p class="text-xs font-weight-bold mb-0">{{ favorite.category }}</p>
                </td>
                <td class="align-middle text-center">
                  <span class="text-secondary text-xs font-weight-bold">{{ favorite.date }}</span>
                </td>
                <td class="align-middle text-center">
                  <a href="javascript:;" class="text-secondary font-weight-bold text-xs" @click="deleteFavorite(favorite.dishname)">
                    删除
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Pagination -->
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
  margin-top: 20px;
}
</style>
