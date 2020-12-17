#include <iostream>

constexpr int LEN_INITAL = 8;
constexpr int STEPS = 6;

constexpr int LEN_W = 1 + 2 * STEPS;
constexpr int LEN_Z = LEN_W;
constexpr int LEN_Y = LEN_INITAL + 2 * STEPS;
constexpr int LEN_X = LEN_INITAL + 2 * STEPS;
constexpr int LEN_TOTAL = LEN_W * LEN_Z * LEN_Y * LEN_X;

constexpr int SIZE_W = LEN_Z * LEN_Y * LEN_X;
constexpr int SIZE_Z = LEN_Y * LEN_X;
constexpr int SIZE_Y = LEN_X;

constexpr int NUM_THREADS = 512;
constexpr int NUM_BLOCKS = LEN_TOTAL / NUM_THREADS;

inline int coord_to_idx(const int w, const int z, const int y, const int x) {
  return
    w * SIZE_W +
    z * SIZE_Z +
    y * SIZE_Y +
    x;
}

inline void print_slice(const int* grid, const int w, const int z) {
  for (int row = 0; row < LEN_Y; ++row) {
    for (int col = 0; col < LEN_X; ++col) {
      std::cout << grid[coord_to_idx(w, z, row, col)] << " ";
    }
    std::cout << "\n";
  }
}

__device__
int coord_to_idx_dev(const int w, const int z, const int y, const int x) {
  return w * SIZE_W + z * SIZE_Z + y * SIZE_Y + x;
}

__global__
void step(const int* grid, int* grid_next) {
  // Find out where we are.
  const int idx = blockIdx.x * blockDim.x + threadIdx.x;
  if (idx < LEN_TOTAL) {
    int left = idx;
    int w = idx / SIZE_W;
    left = idx - w * SIZE_W;
    int z = left / SIZE_Z;
    left = left - z * SIZE_Z;
    int y = left / SIZE_Y;
    int x = left - y * SIZE_Y;

    // TODO: for loop here?
    const int active = grid[idx];
    // Count active neighbors.
    int active_neighbors = 0;
    int min_nw = max(0, w - 1);
    int max_nw = min(LEN_W, w + 2);
    int min_nz = max(0, z - 1);
    int max_nz = min(LEN_Z, z + 2);
    int min_ny = max(0, y - 1);
    int max_ny = min(LEN_Y, y + 2);
    int min_nx = max(0, x - 1);
    int max_nx = min(LEN_X, x + 2);
    for (int nw = min_nw; nw < max_nw; ++nw) {
      for (int nz = min_nz; nz < max_nz; ++nz) {
        for (int ny = min_ny; ny < max_ny; ++ny) {
          for (int nx = min_nx; nx < max_nx; ++nx) {
            active_neighbors += grid[coord_to_idx_dev(nw, nz, ny, nx)];
          }
        }
      }
    }
    active_neighbors -= active;
    // Rules
    int active_next = active;
    if (active == 1 && (active_neighbors < 2 || active_neighbors > 3)) {
      active_next = 0;
    }
    else if (active == 0 && active_neighbors == 3) {
      active_next = 1;
    }
    //active_next = idx;
    grid_next[idx] = active_next;
  }
}

int main() {

  // Initialize grid.
  int* grid;
  cudaMallocManaged(&grid, LEN_TOTAL * sizeof(int));
  cudaMemset(grid, 0, LEN_TOTAL);
  int initial_grid[LEN_INITAL][LEN_INITAL] = {
    {1, 1, 0, 0, 1, 0, 1, 0},
    {1, 1, 1, 0, 1, 0, 1, 1},
    {0, 0, 1, 1, 1, 0, 0, 1},
    {0, 1, 0, 0, 0, 0, 1, 1},
    {0, 1, 0, 0, 1, 1, 1, 1},
    {1, 1, 1, 1, 1, 0, 0, 0},
    {1, 1, 1, 1, 1, 1, 1, 0},
    {1, 0, 1, 1, 0, 1, 0, 1}
  };
  for (int row = 0; row < LEN_INITAL; ++row) {
    for (int col = 0; col < LEN_INITAL; ++col) {
      grid[coord_to_idx(STEPS, STEPS, STEPS + row, STEPS + col)] = initial_grid[row][col];
    }
  }
  //print_slice(grid, STEPS, STEPS);
  int* grid_next;
  cudaMallocManaged(&grid_next, LEN_TOTAL * sizeof(int));
  for (int i = 0; i < STEPS; ++i) {
    //std::cout << "Step " << i << "\n";
    step<<<NUM_BLOCKS, NUM_THREADS>>>(grid, grid_next);
    cudaDeviceSynchronize();
    std::swap(grid, grid_next);
    //print_slice(grid, STEPS, STEPS);
  }
  // Count actives.
  int count = 0;
  for (int i = 0; i < LEN_TOTAL; ++i) {
    count += grid[i];
  }
  std::cout << "Active: " << count << "\n";
  cudaFree(grid);
  cudaFree(grid_next);
  return 0;
}
