<script setup>
import { ref, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Mock from 'mockjs';
import axios from 'axios';

const isFavorited = ref(false); // 记录是否已收藏
const router = useRouter(); // 获取路由实例

// Mock收藏接口
Mock.mock('http://localhost:5000/add_to_collection', 'post', (options) => {
  const { foodName, timestamp } = JSON.parse(options.body);
  return {
    status: 200,
    message: `已成功收藏 ${foodName} 于 ${timestamp}`,
    data: { dishname: foodName, category: '未知分类', date: timestamp }
  };
});

// 获取路由参数
const route = useRoute();
const foodId = Number(route.params.id);

// 示例食物数据
const foods = [
  { id: 1, name: "食物 A", ingredients: "鸡肉, 蘑菇, 酱油", images: ["https://via.placeholder.com/300"] },
  { id: 2, name: "食物 B", ingredients: "牛肉, 青椒, 大葱", images: ["https://via.placeholder.com/300"] },
];

// 获取食物信息
const food = foods.find(f => f.id === foodId) || { name: "未知食物", ingredients: "", images: [] };
const foodImages = ref(food.images);

// 评论数据
const comments = ref([
  { user: "User2", avatar: "https://via.placeholder.com/50", message: "味道还不错，但略微偏咸。", rating: 4.5 },
  { user: "User1", avatar: "https://via.placeholder.com/50", message: "这道菜非常好吃！", rating: 5 },
]);

const newComment = ref("");
const valueHalf = ref(); // 用于评分组件的变量

// 收藏功能
const addToCollection = async () => {
  const foodName = food.name;
  const timestamp = new Date().toLocaleString();

  try {
    const response = await axios.post('http://localhost:5000/add_to_collection', { foodName, timestamp });
    if (response.status === 200) {
      isFavorited.value = true;
      alert(response.data.message);
      // 跳转到我的收藏页面并传递收藏信息
      router.push({ 
        path: '/collection', 
        query: { foodName, timestamp } // 传递菜名和时间
      });
    } else {
      console.error('添加收藏失败:', response.data.message);
    }
  } catch (error) {
    console.error('添加收藏时出错:', error);
  }
};

// 评分变化处理函数
const change = (value) => {
  console.log("评分已更改为:", value);
  valueHalf.value = value;
};

// 添加评论
const addComment = () => {
  if (newComment.value.trim() === "") {
    alert("评论内容不能为空。");
    return;
  }
  comments.value.unshift({
    user: "当前用户",
    avatar: "https://via.placeholder.com/50",
    message: newComment.value,
    rating: valueHalf.value || 0,
  });
  newComment.value = "";
  scrollToTop();
};

const scrollToTop = () => {
  nextTick(() => {
    const commentsArea = document.querySelector('.comments-area');
    commentsArea.scrollTop = 0;
  });
};
</script>

<template>
  <div class="container">
    <div class="row">
      <!-- 左侧固定部分 -->
      <div class="col-lg-4" style="position: sticky; top: 20px;">
        <div class="mb-4">
          <h5>{{ food.name }}</h5>
        </div>
        <div class="card mb-4">
          <img :src="foodImages[0]" class="carousel-img" alt="Food Image" />
        </div>
        <div class="card">
          <div class="card-body">
            <div class="mb-3">
              <label for="ingredients" class="form-label">原料</label>
              <input 
                type="text" 
                id="ingredients" 
                class="form-control" 
                :value="food.ingredients" 
                readonly 
              />
            </div>
            <div>
              <label for="rating" class="form-label">评分</label>
              <d-rate 
                type="warning" 
                v-model="valueHalf" 
                :allow-half="true" 
                @change="change" 
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧评论区 -->
      <div class="col-lg-8">
        <div class="d-flex justify-content-end mb-2">
          <button 
            class="btn btn-primary btn-sm" 
            @click="addToCollection" 
            :disabled="isFavorited"
          >
            {{ isFavorited ? '已收藏' : '收藏' }}
          </button>
        </div>

        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">评论区</h5>
          </div>

          <div class="card-body comments-area" ref="commentsArea">
            <div v-for="(comment, index) in comments" :key="index" class="mb-4 d-flex align-items-center">
              <img :src="comment.avatar" alt="User Avatar" class="rounded-circle me-3" width="50" height="50" />
              <div class="flex-grow-1">
                <h6 class="mb-0">{{ comment.user }}</h6>
                <p class="mb-0">{{ comment.message }}</p>
                <d-rate type="warning" :read="true" v-model="comment.rating" />
              </div>
            </div>
          </div>
        </div>

        <div class="fixed-input-container">
          <input 
            type="text" 
            v-model="newComment" 
            class="form-control" 
            placeholder="添加评论..." 
          />
          <button class="btn btn-primary btn-sm mt-2" @click="addComment">提交</button>
        </div>
      </div>
    </div>

    <div v-if="!food.id" class="alert alert-danger mt-4">
      未找到食物信息，请检查链接是否正确。
    </div>
  </div>
</template>

<style scoped>
/* 左侧固定样式 */
.col-lg-4 {
  height: fit-content;
}

/* 收藏按钮 */
.btn-sm {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
}

/* 固定输入框样式 */
.fixed-input-container {
  position: sticky;
  bottom: 0;
  background-color: white;
  padding: 10px;
  box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
}

.fixed-input-container input {
  width: 75%;
  margin-right: 10px;
}

/* 评论区样式 */
.comments-area {
  overflow-y: auto;
  max-height: 240px;
  height: 240px;
}

/* 图片样式 */
.carousel-img {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* 固定输入框样式 */
.fixed-input-container {
  position: sticky; /* 固定在底部 */
  bottom: 0;
  background-color: white; /* 背景颜色 */
  padding: 10px;
  box-shadow: 0 -1px 5px rgba(0, 0, 0, 0.1);
  margin-top: 20px; /* 增加上边距 */
}

</style>
