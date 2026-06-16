import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import KnowledgeList from './pages/KnowledgeList';
import KnowledgeDetail from './pages/KnowledgeDetail';
import Search from './pages/Search';
import Categories from './pages/Categories';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="knowledge" element={<KnowledgeList />} />
          <Route path="knowledge/:id" element={<KnowledgeDetail />} />
          <Route path="search" element={<Search />} />
          <Route path="categories" element={<Categories />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
