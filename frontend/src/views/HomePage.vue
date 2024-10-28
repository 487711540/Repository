<template>
  <div class="container">
    <div class="dropdowns mb-4">
      <select class="form-select" v-model="selected1">
        <option disabled value="">大类</option>
        <option>选项 A</option>
        <option>选项 B</option>
        <option>选项 C</option>
      </select>

      <select class="form-select" v-model="selected4">
        <option disabled value="">小类</option>
        <option>选项 J</option>
        <option>选项 K</option>
        <option>选项 L</option>
      </select>

      <d-button class="btn btn-refresh" @click="refreshRankings">刷新排行榜</d-button>
    </div>

    <div class="content-boxes row">
      <!-- 个性化推荐区域 -->
      <div class="box col-6 mb-4">
        个性化推荐
        <div class="card mb-4 cool-carousel">
          <d-carousel height="300px" autoplay :autoplay-speed="3000" transition="ease">
            <d-carousel-item class="d-carousel-item cool-carousel-item" v-for="(item) in foodImages" :key="item.id">
              <img :src="item.src" class="carousel-img" alt="Food Image" @click="handleImageClick(item.id)" />
            </d-carousel-item>
          </d-carousel>
        </div>
      </div>
      
      <!-- 排行榜区域 -->
      <div class="box col-6 mb-4">
        排行榜
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">序号</th>
              <th scope="col">食物名称</th>
              <th scope="col">评分</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in rankings" :key="item.id" @click="handleRankingClick(item.id)">
              <td>{{ index + 1 }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.rating }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();

// 下拉框选择项
const selected1 = '';
const selected4 = '';

// 轮播图数据
const foodImages = ref([
  { id: 1, src: "https://via.placeholder.com/300" },
  { id: 2, src: "https://via.placeholder.com/300/ff0000" },
  { id: 3, src: "https://via.placeholder.com/300/00ff00" },
  { id: 4, src: "https://via.placeholder.com/300/0000ff" },
]);

// 排行榜数据
const rankings = ref([
  { id: 1, name: '食物 A', rating: 4.5 },
  { id: 2, name: '食物 B', rating: 4.2 },
  { id: 3, name: '食物 C', rating: 4.8 },
]);

const handleImageClick = (id) => {
  console.log(`点击了图片，准备跳转到个性化页面，id: ${id}`);
  router.push({ name: '个性化推荐', params: { id } });
};

const handleRankingClick = (id) => {
  console.log(`点击了排行榜，准备跳转到个性化页面，id: ${id}`);
  router.push({ name: '个性化推荐', params: { id } });
};


// 刷新排行榜
const refreshRankings = () => {
  console.log('排行榜已刷新！');
  // 可以在这里添加实际的刷新逻辑
};
</script>

<style scoped>
.container {
  padding: 20px;
}

.dropdowns {
  display: flex;
  justify-content: space-between;
}

.form-select {
  flex: 1;
  margin-right: 10px;
}

.form-select:last-child {
  margin-right: 0;
}

.content-boxes {
  display: flex;
  gap: 20px;
}

.box {
  border: 1px solid #ccc;
  height: auto;
  text-align: center;
  padding: 20px;
  flex: 1;
  background-color: aqua;
}

.btn-refresh {
  padding: 10px 20px;
  font-size: 16px;
  margin-left: 10px;
}

.cool-carousel {
  margin-top: 20px;
}

.carousel-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: pointer;
}

.table {
  width: 100%;
  margin-top: 20px;
}

.table-striped tbody tr {
  cursor: pointer;
}
</style>
