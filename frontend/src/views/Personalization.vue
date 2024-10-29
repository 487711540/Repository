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

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();

const food = ref({});
const foodImages = ref([]);
const comments = ref([]);
const newComment = ref('');
const isFavorited = ref(false);
const valueHalf = ref(0);

// 组件挂载时获取食物信息
onMounted(async () => {
  const foodName = route.params.foodName; // 从路由参数中获取食物名称
  await fetchFoodData(foodName);
  await fetchComments(foodName);
});

// 获取食物数据
const fetchFoodData = async (name) => {
  try {
    const response = await axios.get(`http://localhost:5000/food?name=${name}`);
    if (response.data.code === 200) {
      food.value = response.data.data;
      foodImages.value = food.value.images; // 假设图片数组
    } else {
      console.error(response.data.msg);
    }
  } catch (error) {
    console.error('获取食物数据失败:', error);
  }
};

// 获取评论数据
const fetchComments = async (foodName) => {
  try {
    const response = await axios.get(`http://localhost:5000/comments?foodName=${foodName}`);
    if (response.data.code === 200) {
      comments.value = response.data.data; // 评论数据
    } else {
      console.error(response.data.msg);
    }
  } catch (error) {
    console.error('获取评论数据失败:', error);
  }
};

// 添加评论
const addComment = async () => {
  if (newComment.value.trim() === '') return;
  
  // 发送评论数据到后端
  try {
    const response = await axios.post('http://localhost:5000/comments', {
      foodName: food.value.name,
      message: newComment.value,
      rating: valueHalf.value,
    });
    if (response.data.code === 200) {
      comments.value.push({
        user: '当前用户', // 替换为实际用户信息
        avatar: '用户头像路径', // 替换为实际用户头像
        message: newComment.value,
        rating: valueHalf.value,
      });
      newComment.value = ''; // 清空输入框
      valueHalf.value = 0; // 重置评分
    } else {
      console.error(response.data.msg);
    }
  } catch (error) {
    console.error('添加评论失败:', error);
  }
};

// 添加到收藏
const addToCollection = async () => {
  // 处理收藏逻辑
  isFavorited.value = true;
};

// 评分改变
const change = (value) => {
  console.log(`评分改变: ${value}`);
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.fixed-input-container {
  position: sticky;
  bottom: 20px;
  left: 0;
  right: 0;
  background-color: white;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.comments-area {
  max-height: 400px;
  overflow-y: auto;
}
</style>
