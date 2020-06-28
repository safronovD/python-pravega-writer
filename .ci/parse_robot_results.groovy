void parseRobotResults(String outputPath) {
  step([
        $class              : 'RobotPublisher',
        outputPath          :  outputPath,
        outputFileName      : 'output.xml',
        reportFileName      : 'report.html',
        logFileName         : 'log.html',
        disableArchiveOutput: false,
        passThreshold       : 60,
        unstableThreshold   : 40,
        otherFiles          : "**/*.png,**/*.jpg",
  ]);
}
return this