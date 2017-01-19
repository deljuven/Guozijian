//
//  ViewController.m
//  Guozijian
//
//  Created by 李然 on 2017/1/3.
//  Copyright © 2017年 李然. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    NSURL *url = [NSURL URLWithString:@"http://202.120.40.20:5000"];
    [self.wenView loadRequest:[NSURLRequest requestWithURL:url]];
}




- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


@end
