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
              <label for="rating" class="form-label">评分</label>
              <d-rate type="warning" v-model="food.score" :allow-half="true" @change="change" />
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
          <button class="btn btn-primary btn-sm" @click="addToCollection" :disabled="isFavorited">
            {{ isFavorited ? '已收藏' : '收藏' }}
          </button>
        </div>

        <div class="card mb-4">
          <div class="card-header">
            <h5 class="mb-0">评论区</h5>
          </div>
          <div class="card-body comments-area" ref="commentsArea">
            <div v-for="(comment, index) in comments" :key="index" class="mb-4 d-flex align-items-center">
              <img :src="comment.avatar" alt="User Avatar" class="rounded-circle me-3" width="50" height="50" />
              <div class="flex-grow-1">
                <h6 class="mb-0">{{ comment.user || "匿名用户" }}</h6>
                <p class="mb-0">{{ comment.message }}</p>
                <d-rate type="warning" :read="true" v-model="comment.rating" />
              </div>
            </div>
          </div>
        </div>

        <div class="fixed-input-container">
          <d-rate v-model="newRating" type="warning" :allow-half="true" />
          <input type="text" v-model="newComment" class="form-control mt-2" placeholder="添加评论..." />
          <button class="btn btn-primary btn-sm mt-2" @click="addComment">提交</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
import axios from 'axios';

const store = useStore();
const route = useRoute();

const food = ref({});
const foodImages = ref([]);
const comments = ref([]);
const newComment = ref('');
const newRating = ref(0); // 新增评分
const isFavorited = ref(false);

// 组件挂载时获取食物信息
onMounted(async () => {
  const dishname = route.params.name; // 从路由参数中获取菜品名称
  await fetchFoodData(dishname);
  await fetchComments(dishname);
});

// 获取食物数据
const fetchFoodData = async (dishname) => {
  console.log('请求的菜品名称:', dishname);
  const formData = new FormData();
  formData.append('dishname', dishname); // 添加文本字段

  try {
    const response = await axios.post('http://localhost:5000/info', formData);

    if (response.data.code === 200&& response.data.data) {
      food.value = {
        name: response.data.data.dishname,
        bigtype: response.data.data.bigtype,
        desc: response.data.data.desc,
        img: response.data.data.img,
        score: response.data.data.score,
      };

      if (response.data.data.images && response.data.data.images.length) {
        foodImages.value = response.data.data.images.map((img, index) => ({
          id: `${dishname}-${index}`,
          img: img.url || response.data.data.img,
        }));
      } else {
        foodImages.value = [{ id: `${dishname}-0`, img: response.data.data.img }];
      }
    } else {
      console.error("Error message:", response.data.msg);
    }
  } catch (error) {
    console.error('Error fetching food data:', error);
  }
};

// 获取评论数据
const fetchComments = (dishname) => {
  if (!dishname) return;

  const formData = new FormData();
  formData.append('dishname', dishname); // 添加文本字段

  axios.post(`http://localhost:5000/dishname_comment`, formData)
    .then(response => {
      if (response.data.code === 200) {
        comments.value = response.data.data.map(comment => ({
          user: comment[0] || "匿名用户",
          avatar: comment[1] || "默认头像路径", // 替换为实际头像路径
          message: comment[2],
          rating: comment[3],
        }));
      } else {
        console.error("Error message:", response.data.msg);
      }
    })
    .catch(error => {
      console.error('Error fetching comments:', error);
    });
};

// 添加评论
const addComment = () => {
  if (!newComment.value || newRating.value === 0) {
    console.error('评论内容和评分不能为空');
    return;
  }

  const formData = new FormData();
  const userName = store.state.username; // 从 Vuex 获取用户名
  formData.append('username', userName);
  formData.append('dishname', food.value.name);
  formData.append('comment', newComment.value);
  formData.append('rating', newRating.value); // 添加评分

  axios.post(`http://localhost:5000/comment`, formData)
    .then(response => {
      if (response.data.code === 200) {
        // 将新评论置顶
        comments.value.unshift({
          user: userName,
          avatar: "默认头像路径", // 替换为实际头像路径
          message: newComment.value,
          rating: newRating.value, // 确保评分与评论一一对应
        });
        newComment.value = '';
        newRating.value = 0; // 重置评分
      } else {
        console.error("Error message:", response.data.msg);
      }
    })
    .catch(error => {
      console.error('Error adding comment:', error);
    });
};

// 收藏功能
const addToCollection = () => {
  isFavorited.value = true; // 假设实现收藏逻辑
};

</script>

<style scoped>
.carousel-img {
  width: 100%;
  height: 200px;
  /* 设置固定高度 */
  object-fit: cover;
  /* 确保图片按比例填充，裁剪多余部分 */
}

.fixed-input-container {
  position: fixed;
  bottom: 20px;
  width: calc(100% - 30px);
  /* 减去一些边距 */
  padding: 20px;
  background: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  /* 添加阴影效果 */
  margin-top: 20px;
  /* 添加与评论区的边距 */
}

.comments-area {
  max-height: 300px;
  /* 设置最大高度 */
  overflow-y: auto;
  /* 允许垂直滚动 */
  margin-bottom: 20px;
  /* 添加评论区与输入区的边距 */
}
</style>
