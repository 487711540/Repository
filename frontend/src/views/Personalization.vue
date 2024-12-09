<template>
  <div class="container">
    <div class="row">
      <!-- 左侧固定部分 -->
      <div class="col-lg-4" style="position: sticky; top: 20px;">
        <div class="mb-4">
          <h5>{{ food.name || '未找到食物信息' }}</h5>
        </div>
        <div class="card mb-4">
          <img v-if="foodImages.length" :src="foodImages[0].img" class="carousel-img" alt="Food Image" />
        </div>
        <div class="card">
          <div class="card-body">
            <div class="mb-3">
              <label for="type" class="form-label">菜系</label>
              <input type="text" id="type" class="form-control" :value="food.bigtype || '无信息'" readonly />
            </div>
            <div class="mb-3">
              <label for="rating" :value="food.score" class="form-label">评分</label>
              <d-rate type="warning" v-model="newRating" :allow-half="true" @dblclick="addScore" />
            </div>
            <div class="mt-3">
              <label for="desc" class="form-label">描述</label>
              <textarea id="desc" class="form-control" rows="3" :value="food.desc || '无描述信息'" readonly></textarea>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧评论区 -->
      <div class="col-lg-8">
        <div class="d-flex justify-content-end mb-2">
          <button class="btn btn-primary btn-sm" @click="addToCollection" :disabled="isLoading">
            {{ isFavorited ? '已收藏' : '收藏' }}
          </button>
        </div>

        <div class="card mb-4">
          <div class="card-header">
            <h5 class="mb-0">评论区</h5>
          </div>
          <div class="card-body comments-area" ref="commentsArea">
            <div v-for="(comment, index) in comments" :key="index" class="mb-4 d-flex align-items-center">
              <img src="@/views/useravatar.jpg" alt="User Avatar" class="rounded-circle me-3" width="50" height="50" />
              <div class="flex-grow-1">
                <h6 class="mb-0">{{ comment.user || "匿名用户" }}</h6>
                <p class="mb-0">{{ comment.avatar }}</p>
                <d-rate type="warning" :read="true" :allow-half="true" v-model="comment.message" />
              </div>
            </div>
          </div>
        </div>

        <div class="fixed-input-container">
          <!-- <d-rate v-model="newRating" type="warning" :allow-half="true" /> -->
          <input width="500" type="text" v-model="newComment" class="form-control mt-2" placeholder="添加评论..." />
          <button class="btn btn-primary btn-sm mt-2" @click="addComment">提交</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
import axios from 'axios';
//import { useRouter } from 'vue-router';

//const router = useRouter();
const store = useStore();
const route = useRoute();

const food = ref({});
const foodImages = ref([]);
const comments = ref([]);
const newComment = ref('');
const newRating = ref(0); // 新增评分
const isFavorited = ref(false);
const isLoading = ref(false); // 控制按钮加载状态


const isCommentAdded = ref(false); // 用于监视评论是否已添加
const isRatingAdded = ref(false); // 用于监视评论是否已添加

// 组件挂载时获取食物信息
onMounted(async () => {
  const dishname = route.params.name; // 从路由参数中获取菜品名称
  await fetchFoodData(dishname);
  await fetchComments(dishname);
  loadUserRating(dishname); // 加载用户评分

  //await checkIfFavorited(dishname); // 检查菜品是否被收藏
  checkIfFavorited();
});


// 检查菜品是否被收藏
const checkIfFavorited = async (/* dishname */) => {
  const formData = new FormData();
  formData.append('dishname', /* dishname */food.value.name);
  formData.append('username', store.state.username);

  try {
    const response = await axios.post('http://localhost:5000/check_favorites', formData);
    if (response.data.code === 200) {
      isFavorited.value = response.data.data.isFavorited; // 根据返回值设置收藏状态
    } else {
      console.error("检查收藏状态失败:", response.data.msg);
    }
  } catch (error) {
    console.error('检查收藏状态时出错:', error);
  }
};

// 监视评论是否已添加
watch(isCommentAdded, async (newValue) => {
  if (newValue) {
    const dishname = food.value.name; // 获取菜品名称
    await fetchComments(dishname); // 重新获取评论
    isCommentAdded.value = false; // 重置状态

    // router.go(0);
  }
});

// 监视评分是否已添加
watch(isRatingAdded, async (newValue) => {
  if (newValue) {
    const dishname = food.value.name; // 获取菜品名称
    await fetchComments(dishname); // 重新获取评论
    isRatingAdded.value = false; // 重置状态

    // router.go(0);
  }
});

// 获取食物数据
const fetchFoodData = async (dishname) => {
  const formData = new FormData();
  formData.append('dishname', dishname); // 添加文本字段

  try {
    const response = await axios.post('http://localhost:5000/info', formData);
    if (response.data.code === 200 && response.data.data) {
      food.value = {
        name: response.data.data.dishname,
        bigtype: response.data.data.bigtype,
        desc: response.data.data.desc,
        img: response.data.data.img,
        score: response.data.data.score,
      };
    
      foodImages.value = response.data.data.images?.map((img, index) => ({
        id: `${dishname}-${index}`,
        img: img.url || response.data.data.img,
      })) || [{ id: `${dishname}-0`, img: response.data.data.img }];
    } else {
      console.error("Error message:", response.data.msg);
    }
  } catch (error) {
    console.error('Error fetching food data:', error);
  }
};

// 获取评论数据
const fetchComments = async (dishname) => {
  if (!dishname) return;

  const formData = new FormData();
  formData.append('dishname', dishname);

  try {
    const response = await axios.post('http://localhost:5000/dishname_comment', formData);
    if (response.data.code === 200) {
      console.log(response.data);
      comments.value = response.data.data.map(comment => ({
        user: comment[0] || "匿名用户",
        avatar: comment[1] , // 确保头像路径正确
        message: parseFloat(comment[2]),
             
       
      }));
    } else {
      console.error("Error message:", response.data.msg);
    }
  } catch (error) {
    console.error('Error fetching comments:', error);
  }
};

// 加载用户评分
const loadUserRating = (dishname) => {
  const savedRating = localStorage.getItem(`rating_${dishname}`);
  newRating.value = savedRating !== null ? parseFloat(savedRating) : 0; // 初始化评分
};



// 添加评分
const addScore = async () => {
  const formData = new FormData();
  const userName = store.state.username;
  formData.append('username', userName);
  formData.append('dishname', food.value.name);
  formData.append('score', newRating.value); // 确保使用 'score' 字段

  try {
    const response = await axios.post('http://localhost:5000/rate', formData);
    if (response.data.code === 200) {
      localStorage.setItem(`rating_${food.value.name}`, newRating.value); // 保存评分
      isRatingAdded.value = true;
      console.log('评分成功:', response.data);
      alert('评分成功！'); // 显示成功提示
      return true; // 评分成功返回 true
    } else {
      console.error("评分失败:", response.data.msg);
      alert('评分失败: ' + response.data.msg); // 显示失败提示
      return false; // 评分失败返回 false
    }
  } catch (error) {
    console.error('添加评分时出错:', error);
    alert('评分时出错，请稍后再试。'); // 显示错误提示
    return false; // 发生错误返回 false
  }
};

// 添加评论
const addComment = async () => {
  if (!newComment.value.trim()) {
    console.error('评论内容不能为空');
    alert('评论内容不能为空');
    return;
  }
  if (!newRating.value) {
    console.error('请先为菜品评分');
    alert('请先为菜品评分');
    return false; // 如果没有评分，直接返回
  }

  // 首先添加评分
  //const scoreSuccess = await addScore();
  //if (scoreSuccess) {
    const formData = new FormData();
    const userName = store.state.username;
    formData.append('username', userName);
    formData.append('dishname', food.value.name);
    formData.append('comment', newComment.value);

    try {
      const response = await axios.post('http://localhost:5000/comment', formData);
      if (response.data.code === 200) {
        isCommentAdded.value = true; // 标记评论已添加
        //console.log('评论成功:', response.data);
        alert('评论成功！'); // 显示成功提示
        newComment.value = ''; // 清空评论输入框
        //newRating.value = 0; // 重置评分
      } else {
        console.error("评论失败:", response.data.msg);
        alert('评论失败: ' + response.data.msg); // 显示失败提示
      }
    } catch (error) {
      console.error('添加评论时出错:', error);
      alert('评论时出错，请稍后再试。'); // 显示错误提示
    }
  //}
};


// 收藏功能
const addToCollection = async () => {
  const dishname = food.value.name;
  if (!dishname) return;

  const formData = new FormData();
  formData.append('dishname', dishname);
  formData.append('username', store.state.username);

  isLoading.value = true; // 开始加载

  try {
    if (isFavorited.value) {
      const response = await axios.post('http://localhost:5000/delete_favorites', formData);
      if (response.data.code === 200) {
        isFavorited.value = false;
        alert('取消收藏成功！');
      }
    } else {
      const response = await axios.post('http://localhost:5000/favorites', formData);
      if (response.data.code === 200) {
        isFavorited.value = true;
        alert('收藏成功！');
      }
    }
  } catch (error) {
    console.error('操作时出错:', error);
    alert('操作时出错，请稍后再试。');
  } finally {
    isLoading.value = false; // 操作完成后结束加载
  }
};


</script>


<style scoped>
.carousel-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.fixed-input-container {
  position: fixed;
  bottom: 20px;
  width: calc(100% - 30px);
  padding: 20px;
  background: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.comments-area {
  height: 330px;
  overflow-y: auto;
  margin-bottom: 20px;
}
</style>
