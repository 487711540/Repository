<script setup>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import { useRoute, useRouter } from "vue-router";
import Breadcrumbs from "../Breadcrumbs.vue";
import axios from "axios";

const showMenu = ref(false);
const store = useStore();
const router = useRouter();
const isRTL = computed(() => store.state.isRTL);
const route = useRoute();

const username = computed(() => store.state.username);
const currentDirectory = computed(() => {
  let dir = route.path.split("/")[1];
  return dir.charAt(0).toUpperCase() + dir.slice(1);
});

// 搜索相关
const searchKey = ref('');
const searchResults = ref([]); // 存储搜索结果
const source = ref([]); // 源数据
const allowEmptyValueSearch = ref(true);
const position = ref(['bottom']);

// 获取搜索建议
const fetchSearchResults = async (key) => {
  if (key) {
    const formData = new FormData();
    formData.append('key', key);

    try {
      const response = await axios.post('http://localhost:5000/search', formData);
      if (response.data.code === 200) {
        searchResults.value = response.data.data; // 更新搜索结果
        source.value = searchResults.value; // 更新源数据
        console.log(response.data);
      }
    } catch (error) {
      console.error('搜索请求失败:', error);
    }
  } else {
    searchResults.value = []; // 清空结果
  }
};

//点击搜索结果
// const handleSearchResultClick = (dishname) => {
//   navigateToFoodDetail(dishname); // 跳转到详细界面
// };


// const handleSearchResultClick = (dishname) => {
//   if (dishname) {
//     navigateToFoodDetail(dishname); // 跳转到当前输入的食物详情
//     console.log(1);
    
//   }
// };

// 点击放大镜图标
const search = () => {
  console.log(1);
  
  if (searchKey.value) {
    navigateToFoodDetail(searchKey.value); // 跳转到当前输入的食物详情
    console.log(1);
    
  }
};

// 通用跳转函数
const navigateToFoodDetail = (dishname) => {
  router.replace({ name: '个性化推荐', params: { name: dishname } }); // 跳转到个性化推荐页面
  setTimeout(() => {
    router.go(0);
  }, 0); // 使用 setTimeout 确保在跳转后执行
};

const goToLogin = () => {
  router.push({ name: 'Signin' });
};

const login = (usernameFromDb) => {
  if (usernameFromDb) {
    store.commit("setUsername", usernameFromDb);
  }
};
</script>

<template>
  <nav class="navbar navbar-main navbar-expand-lg px-0 mx-4 shadow-none border-radius-xl"
    :class="isRTL ? 'top-0 position-sticky z-index-sticky' : ''" v-bind="$attrs" id="navbarBlur" data-scroll="true">
    <div class="px-3 py-1 container-fluid">
      <breadcrumbs :current-page="currentRouteName" :current-directory="currentDirectory" />

      <div class="mt-2 collapse navbar-collapse mt-sm-0 me-md-0 me-sm-4" :class="isRTL ? 'px-0' : 'me-sm-4'"
        id="navbar">
        <div class="pe-md-3 d-flex align-items-center" :class="isRTL ? 'me-md-auto' : 'ms-md-auto'">
          
          <div class="dianping-button-container">
            <a href="https://www.dianping.com" class="dianping-button" target="_blank">
              <i class="fa fa-star"></i> 大众点评
            </a>
          </div>

          <span @click="search" class="search-icon">🔍</span>
          <d-auto-complete
            v-model="searchKey"
            :delay="1000"
            :source="source"
            :allow-empty-value-search="allowEmptyValueSearch"
            :position="position"
            :width="220"
            :append-to-body="false"
            @input="fetchSearchResults(searchKey)"
            @keydown.enter="search"     
          >
          </d-auto-complete>
          
          <!-- <ul class="dropdown-menu" v-if="searchKey && searchResults.length">
            <li v-for="food in searchResults" :key="food">
              <a href="#" @click.prevent="handleSearchResultClick(food)" class="dropdown-item">{{ food }}</a>
            </li>
          </ul> -->
        </div>
        <ul class="navbar-nav justify-content-end">
          <li class="nav-item d-flex align-items-center">
            <router-link to="#" @click.prevent="username === '游客' ? goToLogin() : login()"
              class="px-0 nav-link font-weight-bold text-white" target="_blank">
              <i class="fa fa-user" :class="isRTL ? 'ms-sm-2' : 'me-sm-2'"></i>
              <span class="d-sm-inline d-none">{{ username }}</span>
            </router-link>
          </li>
          <li class="nav-item d-xl-none ps-3 d-flex align-items-center">
            <a href="#" @click="minimizeSidebar" class="p-0 nav-link text-white" id="iconNavbarSidenav">
              <div class="sidenav-toggler-inner">
                <i class="sidenav-toggler-line bg-white"></i>
                <i class="sidenav-toggler-line bg-white"></i>
                <i class="sidenav-toggler-line bg-white"></i>
              </div>
            </a>
          </li>
          <li class="px-3 nav-item d-flex align-items-center">
            <a class="p-0 nav-link text-white" @click="toggleConfigurator">
              <i class="cursor-pointer fa fa-cog fixed-plugin-button-nav"></i>
            </a>
          </li>
          <li class="nav-item dropdown d-flex align-items-center" :class="isRTL ? 'ps-2' : 'pe-2'">
            <a href="#" class="p-0 nav-link text-white" :class="[showMenu ? 'show' : '']" id="dropdownMenuButton"
              data-bs-toggle="dropdown" aria-expanded="false" @click="showMenu = !showMenu" @blur="closeMenu">
              <i class="cursor-pointer fa fa-bell"></i>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.dianping-button-container {
  margin-right: 10px; /* 按钮与搜索框之间的间距 */
}

.dianping-button {
  background-color: #FF6A00; /* 大众点评主色 */
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 12px; /* 调整内边距 */
  cursor: pointer;
  text-decoration: none;
  font-size: 14px; /* 调整字体大小 */
  display: flex;
  align-items: center; /* 垂直居中 */
  transition: background-color 0.3s; /* 添加过渡效果 */
}

.dianping-button:hover {
  background-color: #FF8C00; /* 悬停效果 */
}

.dianping-button i {
  margin-right: 5px; /* 图标与文字之间的间距 */
}

.search-icon {
  font-size: 20px; /* 放大镜图标的大小 */
  transition: transform 0.3s, color 0.3s; /* 添加过渡效果 */
  color: #555; /* 默认颜色 */
  cursor: pointer; /* 默认光标样式 */
}

.search-icon:hover {
  transform: scale(1.2); /* 悬停时放大图标 */
  color: #FF6A00; /* 悬停时颜色变化 */
  cursor: pointer; /* 悬停时光标变为手形 */
}

</style>
