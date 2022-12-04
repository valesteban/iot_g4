/*
Función que implementa deep sleep
*/
void deep_sleep(float operation_time, int32_t time_to_wake_up) {
    uint64_t wakeup_time_sec;

    printf("Time to wake up %d \n", time_to_wake_up);
    printf("Operation time %f \n", operation_time);

    if ((time_to_wake_up - operation_time) > 0) {
        wakeup_time_sec = (uint64_t)(time_to_wake_up - operation_time);
    }
    else {
        wakeup_time_sec = 60;
        printf("tiempo de ejecucion");
    }

    // 
    printf("Enabling timer wakeup, %lld\n", wakeup_time_sec);
    esp_sleep_enable_timer_wakeup(wakeup_time_sec * 1000000); // *1.000.000
    printf("going to sleep for clk...") ;
    esp_deep_sleep_start();
}