<?php
/**
 * Helper file for PhpApcCollector.py 
 * collectes php apc statistics for Graphite with Diamond
 *
 * @author Károly Nagy <dr.karoly.nagy@gmail.com>
 * http://charlesnagy.info/
 * 
 */ 
$cache      = apc_cache_info();
$cache_user = apc_cache_info('user', 1);
$mem        = apc_sma_info();

$stats = array(
    "mem"=>array(
        "segments"       => (int)$mem['num_seg'],
        "segment_size"   => (int)$mem['seg_size'],
        "total"          => (int)$mem['num_seg'] * $mem['seg_size'],
    ),
    "opcode"=>array(
        "files_count"    => (int)$cache['num_entries'],
        "files_size"     => (int)$cache['mem_size'],
        "hits"           => (int)$cache['num_hits'],
        "misses"         => (int)$cache['num_misses'],
        "full_count"     => (int)$cache['expunges'],
    ),
    "user"=>array(
        "vars_count" => (int)$cache_user['num_entries'],
        "vars_size"  => (int)$cache_user['mem_size'],
        "hits"       => (int)$cache_user['num_hits'],
        "misses"     => (int)$cache_user['num_misses'],
        "full_count" => (int)$cache_user['expunges'],
    ),
);

echo json_encode($stats);
