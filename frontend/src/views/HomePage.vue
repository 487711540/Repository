<template>
  <div class="container">
    <div class="dropdowns mb-4">
      <select class="form-select" v-model="selected1" @change="fetchSubCategories">
        <option disabled value="">选择大类</option>
        <option v-for="(item, index) in categories" :key="index" :value="item">{{ item }}</option>
      </select>

      <select class="form-select" v-model="selected4" @change="fetchRankings">
        <option disabled value="">选择小类</option>
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
            <d-carousel-item v-for="(item) in foodImages" :key="item.id" class="cool-carousel-item">
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
  { img: 'https://i3.meishichina.com/atta/recipe/2024/09/11/202409111726022291787446749884.jpg?x-oss-process=style/p800', name: '麻婆豆腐' },
  { img: 'https://i3.meishichina.com/atta/recipe/2024/08/08/2024080817231025336609052270985.JPG?x-oss-process=style/p800', name: '默认菜品2' },
  { img: 'https://i3.meishichina.com/atta/recipe/2024/09/03/2024090317253472755819538010238.JPG?x-oss-process=style/p800', name: '默认菜品3' },
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
      categories.value = Object.keys(response.data.data);
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
    await fetchRankings();
  } catch (error) {
    console.error('获取小类时出错:', error);
  }
};

// 获取排行榜数据
const fetchRankings = () => {
  const formData = new FormData();
  formData.append('bigtype', selected1.value);
  formData.append('smalltype', selected4.value);

  axios.post('http://localhost:5000/sort', formData)
    .then(response => {
      if (response.data.code === 200) {
        rankings.value = response.data.data;
        console.log('排行榜数据:', rankings.value);
      } else {
        console.error(response.data.msg);
      }
    })
    .catch(error => {
      console.error('获取排行榜数据失败:', error);
    });
};


// 刷新排行榜
const refreshRankings = async () => {
  await fetchRankings();
};

// 获取菜品图片数据
const fetchFoodImages =  (dishname) => {

  if (!dishname) return;

  const formData = new FormData();
  formData.append('dishname', dishname); // 添加文本字段

  axios.post('http://localhost:5000/info', formData)
  .then(
    (response) => {
      console.log(response.data);
      
        if (response.data.code === 200) {
      foodImages.value = response.data.data.images.map((img, index) => ({
        id: `${dishname}-${index}`,
        img: img.url,
      }));}
  })
  .catch((error) => {
    console.error('Error:', error);
  });


  // try {

    
  //   if (response.data.code === 200) {
  //     foodImages.value = response.data.data.images.map((img, index) => ({
  //       id: `${dishname}-${index}`,
  //       img: img.url,
  //     }));
      
  //   } else {
  //     console.error(response.data.msg);
  //   }
  // } catch (error) {
  //   console.error('获取菜品信息失败:', error);
  // }
};

// 点击轮播图项
const handleImageClick = (name) => {
  console.log(`点击了图片，准备跳转到个性化页面，name: ${name}`);
  router.push({ name: '个性化推荐', params: { name: name } }); // 更新为 name
};

// 点击排行榜项
const handleRankingClick = async (item) => {
  console.log(`点击了排行榜项，item:`, item);
  console.log(`点击了排行榜，准备跳转到个性化页面，name: ${item.name}`);
  const obj =  fetchFoodImages(item.name);
  console.log(obj);
  
  router.push({ name: '个性化推荐', params: { name: item.name } }); // 更新为 name
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
