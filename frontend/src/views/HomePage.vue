<template>
  <div class="container">
    <div class="dropdowns mb-4">
      <select class="form-select" v-model="selected1" @change="fetchSubCategories">
        <option disabled value="">大类</option>
        <option v-for="(item, index) in categories" :key="index" :value="item">{{ item }}</option>
      </select>

      <select class="form-select" v-model="selected4" @change="fetchRankings">
        <option disabled value="">小类</option>
        <option v-for="(item, index) in subCategories" :key="index" :value="item">{{ item }}</option>
      </select>

      <d-button class="btn btn-refresh" @click="refreshRankings">刷新排行榜</d-button>
    </div>

    <div class="content-boxes row">
      <!-- 个性化推荐区域 -->
      <div class="box col-6 mb-4">
        个性化推荐
        <div class="card mb-4 cool-carousel">
          <d-carousel v-if="foodImages.length > 0" height="300px" autoplay :autoplay-speed="3000" transition="ease">
            <d-carousel-item class="d-carousel-item cool-carousel-item" v-for="(item) in foodImages" :key="item.id">
              <img :src="item.img" class="carousel-img" alt="Food Image" @click="handleImageClick(item.name)" />
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
            <tr v-for="(item, index) in rankings" :key="item.id" @click="handleRankingClick(item)">
              <td>{{ index + 1 }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.average_score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';

const router = useRouter();

// 下拉框选择项
const selected1 = ref('');
const selected4 = ref('');

// 类别数据
const categories = ref([]);
const subCategories = ref([]);

// 轮播图数据，添加默认图片
const foodImages = ref([
  { id: 'default1', img: 'https://via.placeholder.com/300x200.png?text=默认图片1', name: '默认菜品1' },
  { id: 'default2', img: 'https://via.placeholder.com/300x200.png?text=默认图片2', name: '默认菜品2' },
  { id: 'default3', img: 'https://via.placeholder.com/300x200.png?text=默认图片3', name: '默认菜品3' },
]);

// 排行榜数据
const rankings = ref([]);

// 组件挂载时获取类别数据
onMounted(async () => {
  await fetchCategories();
});

// 获取类别数据
const fetchCategories = async () => {
  try {
    const response = await axios.get('http://localhost:5000/classes');
    if (response.data.code === 200) {
      categories.value = Object.keys(response.data.data); // 获取大类名称
      if (categories.value.length > 0) {
        selected1.value = categories.value[0];
        await fetchSubCategories();
      }
    }
  } catch (error) {
    console.error('获取类别数据时出错:', error);
  }
};

// 根据大类获取小类
const fetchSubCategories = async () => {
  try {
    const response = await axios.get('http://localhost:5000/classes');
    subCategories.value = response.data.data[selected1.value] || [];
    await fetchRankings(); // 小类更新后立即获取排行榜
  } catch (error) {
    console.error('获取小类时出错:', error);
  }
};

// 获取排行榜数据
const fetchRankings = async () => {
  try {
    const response = await axios.post('http://localhost:5000/sort', {
      bigtype: selected1.value,
      smalltype: selected4.value
    });
    if (response.data.code === 200) {
      rankings.value = response.data.data; // 更新排行榜数据
      console.log('排行榜数据:', rankings.value); // 调试信息
    } else {
      console.error(response.data.msg);
    }
  } catch (error) {
    console.error('获取排行榜数据失败:', error);
  }
};

// 刷新排行榜
const refreshRankings = async () => {
  await fetchRankings();
};

// 根据选择的类别获取菜品信息
const fetchFoodImages = async (dishname) => {
  if (!dishname) return;

  try {
    const response = await axios.post('http://localhost:5000/info', { dishname });
    if (response.data.code === 200) {
      foodImages.value = response.data.data.images.map((img, index) => ({
        id: `${dishname}-${index}`, // 确保 id 唯一
        img: img.url, // 假设 img.url 是图片链接
      }));
    } else {
      console.error(response.data.msg);
    }
  } catch (error) {
    console.error('获取菜品信息失败:', error);
  }
};

// 点击轮播图项
const handleImageClick = (name) => {
  console.log(`点击了图片，准备跳转到个性化页面，name: ${name}`);
  router.push({ name: '个性化推荐', params: { id: name } }); // 使用 name 作为参数
};

const handleRankingClick = async (item) => {
  console.log(`点击了排行榜项，item:`, item);
  console.log(`点击了排行榜，准备跳转到个性化页面，name: ${item.name}`); 
  await fetchFoodImages(item.name); 
  router.push({ name: '个性化推荐', params: { id: item.name } }); // 使用 name 作为参数
};

// 监听小类变化时，刷新排行榜
watch(selected4, async () => {
  await fetchRankings();
});
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
