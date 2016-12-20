/* CTEST is a c file for test 
 * ARGS : 
 * ARG1 , MEM USAGE , HOW MANY GB MEM will be used
 * ARG2 , CPU CORES , HOW MANY CPU Cores will be used
 * ARG3 , RUN TIME in sec.
 *   */
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
//#include <unistd.h>
void erro_usage()
{
  printf("Error! Usage : mem(GB) CPU(core) time(sec) \n ; need 3 int(>=1) args ");
  exit( 500 );
}

int main( int argc , char* argv[] ){
  int i;
  int si[3];
  struct timeval starttime , endtime;
  double timeuse = 0;
  int* pm = NULL ;
  int* pm2 = NULL ;

  //int bigdata[2][ 1024][1024][1024] ;
  long long int pnum = 0;
  gettimeofday( &starttime,0);
  printf("Hello for C Test   : "  );
  for (i = 0; i < argc ; i++){
    printf(" %s ", argv[i]);
  }
  
  printf("\n" );
  if( argc != 4 ){
    erro_usage();
  }
  for (i = 0; i < 3 ; i++){
    si[i] = atoi( argv[i+1] );
    if (si[i] < 1 ) {
      erro_usage();
    }
  }
  // malloc memory
  pnum = ( 1024 * 1024 * 1024  )  ; //* si[0] / sizeof(int) )  ;
  pnum = pnum * si[0] / sizeof(int) ;
  printf( "malloc size : %lld  * %d Bite " , pnum , sizeof(int));
  //pm2 = (int *) malloc ( pnum * sizeof(int) ) ;
  pm = (int *) malloc ( pnum * sizeof(int) ) ; 
  //pm =  (int *) calloc ( pnum , sizeof(int)  ) ;
  if ( pm == NULL) {
    printf("Error! Could not alloc memory\n" );
    exit( 300 ) ;    
  }
  // sleep time
  omp_set_num_threads( si[1] );
  while ( timeuse < si[2] ){
    #pragma omp parallel 
    #pragma omp for 
    for(i=0 ; i< pnum ; i++ ){
       pm[i] = pm[i] % ( i + 1) + 1 ;
    }
    gettimeofday( &endtime,0);
    timeuse = 1000000*(endtime.tv_sec - starttime.tv_sec) + endtime.tv_usec - starttime.tv_usec;
    timeuse /=1000000;
  }
  free( pm );
  printf("End OK ! time : %lf \n" , timeuse);
  return( 0 ) ;
}
