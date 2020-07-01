#include "gtest/gtest.h"

#include "adios2.h"
#include "plxr.h"



TEST(PLXR_WRITE_READ, SIMPLE_WRITE) {
    adios2::ADIOS adios(MPI_COMM_WORLD);
    

    plxr::WriteImage();
    ASSERT_EQ(1, 1);
    //ASSERT_EQ(1, 2);
    
}


int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  int result = 0;
  MPI_Init(&argc, &argv);
  result = RUN_ALL_TESTS();
  MPI_Finalize();
  return result;
}


